import pandas as pd

df = pd.read_csv('././open-data/biblio.csv', dtype=str) #./data-processing/biblio/

df_sorted = df.sort_values(by='ANNO')

crete_array = []

# Ancillary refinements
def last_refine(string):
    if string.endswith(".."):
        return string.replace("..", ".")
    elif string.endswith(",."):
        return string.replace(",.", ".")
    else:
        return string

def checkAnno(anno):
    if pd.isna(anno) or anno == "" or anno == "nan":
        return "s.d."
    else:
        return anno
    
def get_author_string(row):
    if pd.isna(row['AUTORE']):
        if not pd.isna(row["CURATORE"]):
            author_string =  row['CURATORE']
        else:
            author_string = "<span style='display:none;'>ZZ</span>S.A."
    else:
        author_string = row['AUTORE']
    return str(author_string)

def get_article(row):
    ref_first = ""
    if not pd.isna(row['AUTORE']):
        ref_first += str(row['AUTORE']) + ", "
    if not pd.isna(row['TITOLO CONTRIBUTO SPECIFICO']):
        ref_first += "«" + str(row['TITOLO CONTRIBUTO SPECIFICO']) + "», "
    ref_first += "<i>" + str(row['TITOLO VOLUME/RIVISTA']) + "</i>, "
    if not pd.isna(row['SPECIFICHE EDIZIONE']):
        ref_first += (str(row['SPECIFICHE EDIZIONE']) + ", ")
    if not pd.isna(row['NOTE GENERALI']):
        ref_first += (row['NOTE GENERALI'] + ", ")

    ref_first +=  checkAnno(row["ANNO"])
    
    if not pd.isna(row["PAGINE"]):
        full_ref = ref_first + ", pp. " + str(row["PAGINE"]) + "."
    else:
        full_ref = ref_first + "."

    return last_refine(full_ref)

def get_monograph(row):
    if pd.isna(row['AUTORE']):
        if not (pd.isna(row['CURATORE'])):
            ref_first =  str(row['CURATORE']) + "(a cura di), "
        else:
            ref_first = ""
    else:
        ref_first = str(row['AUTORE']) + ", "
    ref_first += "<i>" + str(row['TITOLO VOLUME/RIVISTA']) + "</i>, "
    if not pd.isna(row['SPECIFICHE EDIZIONE']):
        ref_first += (str(row['SPECIFICHE EDIZIONE']) + ", ")
    if not pd.isna(row['NOTE GENERALI']):
        ref_first += (row['NOTE GENERALI'] + ", ")
    if not pd.isna(row['LUOGO EDIZIONE']):
        ref_first += (row['LUOGO EDIZIONE'] + ", ")
        
    full_ref = ref_first + str(checkAnno(row["ANNO"])) + "."
    
    return last_refine(full_ref)

def get_essay_in_book(row):
    ref_first = str(row['AUTORE']) + ", «" + str(row['TITOLO CONTRIBUTO SPECIFICO']) + "», in "
    if not pd.isna(row['CURATORE']):
        ref_first += str(row['CURATORE']) + ", "
    ref_first += "<i>" + str(row['TITOLO VOLUME/RIVISTA']) + "</i>, "
    if not pd.isna(row['SPECIFICHE EDIZIONE']):
        ref_first += (str(row['SPECIFICHE EDIZIONE']) + ", ")
    if not pd.isna(row['NOTE GENERALI']):
        ref_first += (row['NOTE GENERALI'] + ", ")
    ref_first += str(row["LUOGO EDIZIONE"]) +  ", " + str(checkAnno(row["ANNO"]))
    if not pd.isna(row["PAGINE"]):
        full_ref = ref_first + ", pp. " + str(row["PAGINE"]) + "."
    else:
        full_ref = ref_first + "."

    return last_refine(full_ref)

def get_thesis(row):
    ref_first = str(row['AUTORE']) + ", <i>" + str(row['TITOLO VOLUME/RIVISTA']) + "</i>, "
    if not pd.isna(row['SPECIFICHE EDIZIONE']):
        ref_first += (str(row['SPECIFICHE EDIZIONE']) + ", ")
    if not pd.isna(row['NOTE GENERALI']):
        ref_first += (str(row['NOTE GENERALI']) + ", ")
    full_ref = ref_first + str(checkAnno(row["ANNO"]))
    return last_refine(full_ref)
    
def get_full_ref(row):
    if row["TIPO"] == "Articolo in periodico":
        return get_article(row)
    if row["TIPO"] == "Monografia":
        return get_monograph(row)
    if "in volume" in row["TIPO"]:
        return get_essay_in_book(row)
    if "Scheda di catalogo" in row["TIPO"]:
        return get_essay_in_book(row)
    if row["TIPO"] == "Tesi":
        return get_thesis(row)

counter = 1
for idx, row in df_sorted.iterrows():

    print("Processing entry n.", counter)
    counter += 1
    print(row["ID"], row["TIPO"])
    ref_html = "<tr><td>" + str(get_author_string(row)) + "</td><td>" + checkAnno(str(row['ANNO'])) + "</td><td>" + (str(get_full_ref(row))) + "</td></tr>"
    
    crete_array.append(ref_html)

crete = "".join(crete_array)

with open("biblio-rows.html", "w") as file:
    file.write(crete)