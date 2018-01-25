class PerformerDetail:
    name = ""
    e_name = ""
    alias = ""
    sex = ""
    bloodtype = ""
    height = ""
    address = ""
    birthady = ""
    constellation = ""
    location = ""
    ResidentialAddress = ""
    school = ""
    BrokerageAgency = ""
    fameyear = ""
    hobby = ""
    Occupation = ""
    weight = ""
    image = ""
    des = ""

    def __init__(self, name, e_name, alias, sex, bloodtype, height, address,
                 birthday, constellation, location, ResidentialAddress, school,
                 BrokerageAgency, fameyear, hobby, Occupation, weight, image, des):
        self.name = name
        self.e_name = e_name
        self.alias = alias
        self.sex = sex
        self.bloodtype = bloodtype
        self.height = height
        self.address = address
        self.birthady = birthday
        self.constellation = constellation  # 星座
        self.location = location          # 出生地
        self.ResidentialAddress = ResidentialAddress
        self.school = school
        self.BrokerageAgency = BrokerageAgency
        self.fameyear = fameyear
        self.hobby = hobby
        self.Occupation = Occupation
        self.weight = weight
        self.image = image
        self.des = des
