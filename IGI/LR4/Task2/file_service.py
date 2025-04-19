import zipfile


class file_service:
    @staticmethod
    def read_file(name):
        with open(name, 'r', encoding='utf-8') as f:
            text = f.read()
        return text

    @staticmethod
    def write_file(lines, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            f.writelines(lines)

    @staticmethod
    def zip_file(filename, zipname):
        with zipfile.ZipFile(zipname, 'w') as zipf:
            zipf.write(filename)

    @staticmethod
    def get_zip_info(zipname, filename):
        with zipfile.ZipFile(zipname, 'r') as zipf:
            info = zipf.getinfo(filename)

        return (zipf.namelist(), info.filename, info.file_size,
                info.compress_size, info.date_time)
