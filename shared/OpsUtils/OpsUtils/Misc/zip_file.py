def zip_file(zip_path,thisFilename_sh,bash_script_IN):
    import time
    from zipfile import ZipFile, ZIP_DEFLATED, ZipInfo
    
    # write with executable permission inside the ZIP
    zi = ZipInfo(thisFilename_sh)
    zi.date_time = time.localtime(time.time())[:6]
    zi.compress_type = ZIP_DEFLATED
    zi.external_attr = 0o100755 << 16   # -rwxr-xr-x on a regular file
    print('zip_path',zip_path)
    with ZipFile(zip_path, "w", ZIP_DEFLATED) as z:
        z.writestr(zi, bash_script_IN)
