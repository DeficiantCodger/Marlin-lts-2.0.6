import os,sys,shutil,marlin
Import("env")

from SCons.Script import DefaultEnvironment
board = DefaultEnvironment().BoardConfig()

def noencrypt(source, target, env):
  firmware = os.path.join(target[0].dir.path, board.get("build.firmware"))
  # do not overwrite encrypted firmware if present
  if not os.path.isfile(firmware):
    shutil.copy(target[0].path, firmware)

if 'offset' in board.get("build").keys():
  LD_FLASH_OFFSET = board.get("build.offset")
  marlin.replace_define("VECT_TAB_OFFSET", LD_FLASH_OFFSET)

  maximum_ram_size = board.get("upload.maximum_ram_size")

  for i, flag in enumerate(env["LINKFLAGS"]):
    if "-Wl,--defsym=LD_FLASH_OFFSET" in flag:
      env["LINKFLAGS"][i] = "-Wl,--defsym=LD_FLASH_OFFSET=" + LD_FLASH_OFFSET
    if "-Wl,--defsym=LD_MAX_DATA_SIZE" in flag:
      env["LINKFLAGS"][i] = "-Wl,--defsym=LD_MAX_DATA_SIZE=" + str(maximum_ram_size - 40)

  if 'firmware' in board.get("build").keys():
    env.AddPostAction("$BUILD_DIR/${PROGNAME}.bin", noencrypt);
