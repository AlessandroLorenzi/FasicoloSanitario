from fuzzywuzzy import process
from parser_raw import ParserRaw

class ParserMaterDomini(ParserRaw):
    ANALISYS_NAMES = [
        "S-COLESTEROLO TOTALE",
        "S-TRIGLICERIDI",
        "S-COLESTEROLO HDL",
        "S-COLESTEROLO LDL",
        "S-ASPARTATO AMINOTRANSFERASI (AST) (GOT)",
        "S-ALANINA AMINOTRANSFERASI (ALT) (GPT)",
        "S-GAMMA GLUTAMMILTRANSPEPTIDASI (GAMMA GT)",
        "S-FOSFATASI ALCALINA",
        "S-LATTICODEIDROGENASI",
        "S-BILIRUBINA TOTALE ",
        "S-BILIRUBINA DIRETTA",
        "S-BILIRUBINA INDIRETTA",
        "S-UREA",
        "S-CREATININA",
        "S-SODIO",
        "S-POTASSIO",
        "S-CLORO",
        "S-CALCIO TOTALE",
        "Proteine",
        "L3-S-IMMUNOGLOBULINE IGA",
        "S-IMMUNOGLOBULINE IGG",
        "S-IMMUNOGLOBULINE IGM",
        "S-FERRO",
        "S-TRANSFERRINA",
        "S-FERRITINA",
        "S-COBALAMINA (VITAMINA B12)",
        "S-FOLATO",
        "S-VITAMINA D",
        "Rapporto albumina / globuline",
        "Albumina",
        "Alfa-1 globuline",
        "Alfa-2 globuline",
        "Beta-1 globuline",
        "Beta-2 globuline",
        "Gamma globuline",
        "Leucociti",
        "Eritrociti",
        "Emoglobina",
        "Ematocrito",
        "Volume medio emazie (MCV)",
        "Indice di anisocitosi (RDW)",
        "Concentrazione emoglobina emazie (MCHC)",
        "Eritroblasti",
        "Piastrine",
        "Volume medio piastrine (MPV)",
        "Emoglobina media emazie (MCH)",
        "Neutrofili relativi",
        "Linfociti relativi",
        "Monociti relativi",
        "Eosinofili relativi",
        "Basofili relativi",
        "Neutrofili assoluti",
        "Linfociti assoluti",
        "Monociti assoluti",
        "Eosinofili assoluti",
        "Basofili assoluti",
    ]


    def get_all_values(self):
        found_values = []
        for a in self.ANALISYS_NAMES:
            found_value = self.value_of(a)
            if found_value is not None:
                found_values.append(found_value)
        return found_values

    def value_of(self, key):
        pdf_content = self.raw_content.split("\n")
        found_key = process.extractOne(key, pdf_content, score_cutoff=90)
        if found_key is None:
            return None
        index = pdf_content.index(found_key[0])
        txt_value = pdf_content[index + 1]
        try:
            return (found_key[0], float(txt_value.replace(",", ".")))
        except ValueError:
            return (found_key[0], txt_value)
