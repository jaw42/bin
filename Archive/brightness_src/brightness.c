#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>

#define MAX_BRIGHTNESS 2800

static char brightness_path[] = "/sys/class/backlight/backlight.12/brightness";

#ifdef BRIGHTNESS_UP
  #define INCREMENT 25
#endif

#ifdef BRIGHTNESS_DOWN
  #define INCREMENT -25
#endif

int main(int argc, char **argv) {
  char brightness_string[5];
  int brightness;
  size_t read;
  int ret;
  FILE *fp = fopen(brightness_path, "r+");
  if (fp == NULL) {
    printf("FAILED to open file (%d, %d).\n", 0, errno);
    return -1;
  }

#ifdef BRIGHTNESS_SET
  if (argc < 1)
  {
    printf("Missing argument (brightness value).\n");
    fclose(fp);
    return -4;
  }

  brightness = atoi(argv[1]);
#else
  read = fread(brightness_string, 1, 5, fp);
  if (read > 5) {
    printf("FAILED to read file (%d, %d).\n", read, errno);
    fclose(fp);
    return -2;
  }

  brightness = atoi(brightness_string);
  brightness += INCREMENT;
#endif

  if (brightness < 0 || brightness > MAX_BRIGHTNESS) {
    printf("Unexpected brightness value: %d.\n", brightness);
    fclose(fp);
    return -3;
  }

  if (brightness > MAX_BRIGHTNESS) {
    brightness = MAX_BRIGHTNESS;
  }

  if (brightness < 100) {
    brightness = 100;
  }

  ret = snprintf(brightness_string, 5, "%d", brightness);
  if (ret < 0) {
    printf("FAILED to convert brightness to string (%d, %d).\n", ret, errno);
    fclose(fp);
    return -4;
  }

  rewind(fp);
  read = fwrite(brightness_string, 1, 5, fp);
  if (read != strlen(brightness_string) + 1) {
    printf("FAILED to write file (%d, %d).\n", read, errno);
    fclose(fp);
    return -5;
  }

  printf("new brightness: %s\n", brightness_string);

  fclose(fp);
  return 0;
}
