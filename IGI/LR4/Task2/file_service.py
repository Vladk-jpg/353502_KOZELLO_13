import zipfile


class FileService:
    """
    A static utility class for basic file operations and ZIP archiving.
    """

    @staticmethod
    def read_file(name):
        """
        Reads and returns the contents of a text file.

        Args:
            name (str): Path to the file to read.

        Returns:
            str: The contents of the file.
        """
        with open(name, 'r', encoding='utf-8') as f:
            text = f.read()
        return text

    @staticmethod
    def write_file(lines, filename):
        """
        Writes a list of strings to a file.

        Args:
            lines (list): List of strings to write.
            filename (str): Path to the file to write to.
        """
        with open(filename, 'w', encoding='utf-8') as f:
            f.writelines(lines)

    @staticmethod
    def zip_file(filename, zipname):
        """
        Archives a single file into a ZIP archive.

        Args:
            filename (str): Path to the file to zip.
            zipname (str): Path to the resulting ZIP file.
        """
        with zipfile.ZipFile(zipname, 'w') as zipf:
            zipf.write(filename)

    @staticmethod
    def get_zip_info(zipname, filename):
        """
        Gets information about a specific file inside a ZIP archive.

        Args:
            zipname (str): Path to the ZIP file.
            filename (str): Name of the file inside the ZIP to get info about.

        Returns:
            tuple: A tuple containing:
                - list of all file names in the ZIP (list)
                - file name (str)
                - original file size (int)
                - compressed file size (int)
                - modification date and time (tuple)
        """
        with zipfile.ZipFile(zipname, 'r') as zipf:
            info = zipf.getinfo(filename)

        return (
            zipf.namelist(),
            info.filename,
            info.file_size,
            info.compress_size,
            info.date_time
        )
