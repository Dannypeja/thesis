import re

def load_bib_entries(bib_file):
    """
    Load entries from the BibTeX file.
    """
    entries = {}
    with open(bib_file, 'r', encoding='utf-8') as f:
        entry_text = ''
        current_key = None
        for line in f:
            line = line.strip()
            if line.startswith('@'):
                if current_key:
                    entries[current_key] = entry_text
                current_key = line.split('{')[1][:-1]
                entry_text = line + '\n'
            else:
                entry_text += line + '\n'

        if current_key:
            entries[current_key] = entry_text

    return entries

def find_missing_citations(tex_file, bib_entries):
    """
    Find citations in the TeX file that do not have exact matches in the BibTeX file.
    """
    with open(tex_file, 'r', encoding='utf-8') as f:
        tex_content = f.read()

    # Define regular expressions for various citation commands
    citation_patterns = [
        r'\\cite\{([^}]*)\}',
        r'\\citeauthor\{([^}]*)\}',
        r'\\citet\{([^}]*)\}',
        r'\\citetitle\{([^}]*)\}',
        r'\\citeyear\{([^}]*)\}',
        # Add more patterns if needed for other citation commands
    ]

    missing_citations = set()

    for pattern in citation_patterns:
        citations = re.findall(pattern, tex_content)
        for citation in citations:
            keys = [key.strip() for key in citation.split(',')]
            for key in keys:
                if key not in bib_entries:
                    missing_citations.add(key)

    return missing_citations

def find_missing_references(tex_file):
    """
    Find references in the TeX file that do not have corresponding labels.
    """
    with open(tex_file, 'r', encoding='utf-8') as f:
        tex_content = f.read()

    ref_calls = re.findall(r'\\ref\{([^}]*)\}', tex_content)
    label_set = set(re.findall(r'\\label\{([^}]*)\}', tex_content))

    missing_references = set(filter(lambda x: x not in label_set, ref_calls))

    return missing_references

def main():
    bib_file = 'bibliography.bib'
    tex_file = 'main.tex'

    bib_entries = load_bib_entries(bib_file)
    missing_citations = find_missing_citations(tex_file, bib_entries)
    missing_references = find_missing_references(tex_file)

    if missing_citations:
        print("Missing citations found:")
        for key in missing_citations:
            print(key)
    else:
        print("No missing citations found.")

    if missing_references:
        print("Missing references found:")
        for key in missing_references:
            print(key)
    else:
        print("No missing references found.")

if __name__ == "__main__":
    main()
