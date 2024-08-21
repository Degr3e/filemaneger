class File:
    def __init__(self, basic, details, name, is_dir, accessed, created, modified, size, type_):
        self.basic = basic
        self.details = details
        self.name = name
        self.is_dir = is_dir
        self.accessed = accessed
        self.created = created
        self.modified = modified
        self.size = size
        self.type = type_
        # self.created = created
        # self.unit = unit
    def __str__(self) -> str:
        return f"{self.basic} ({self.details})"
    # мб гб перевод 
    # def convert_size(self, size, unit):
            
    #     if unit == "b":
    #         return size + unit
    #     elif unit == "kb":
    #         return size / 2**10 + unit
    #     elif unit == "mb":
    #         return size / 2**20 + unit
    #     elif unit == "gb":
    #         return size / 2**30 + unit
    #     elif unit == "tb":
    #         return size / 2**40 + unit
    #     raise ValueError("некоректная единица измерения!")

    def to_dict(self) -> dict:
        return {
            "basic" : self.basic,
            "details" : self.details,
            "created" : self.created
        }