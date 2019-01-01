def read_values(path):
    try:
        values = open(path).read().split("\n")
    except:
        values=input("Değerleri toplu bir şikilde giriniz:\n").split("\n")
    return values