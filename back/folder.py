class Folder:
    def __init__(self, dir, size, created):
        self.dir = dir
        self.size = size
        self.created = created

    def to_dict(self) -> dict:
        return {
            "dir" : self.dir,
            "created" : self.created,
            "size" : self.size,
            "type" : "folder"
        }
    