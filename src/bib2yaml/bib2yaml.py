import argparse
import bibtexparser
import yaml


def convert_bib(input_file: str, output_file: str, n_max_authors: int):
    months_to_num_dict = {
        "jan": 1,
        "january": 1,
        "feb": 2,
        "february": 2,
        "mar": 3,
        "march": 3,
        "apr": 4,
        "april": 4,
        "may": 5,
        "jun": 6,
        "june": 6,
        "jul": 7,
        "july": 7,
        "aug": 8,
        "august": 8,
        "sep": 9,
        "sept": 9,
        "september": 9,
        "oct": 10,
        "october": 10,
        "nov": 11,
        "november": 11,
        "dec": 12,
        "december": 12,
    }

    new_output = []

    def null_checker(bib_entry, key):
        return (
            bib_entry.fields_dict[key].value
            if key in bib_entry.fields_dict
            and bib_entry.fields_dict[key].value is not None
            else None
        )

    library = bibtexparser.parse_file(input_file)

    for entry in library.entries:
        # TODO: Check if the any of the visible name is same as the CV author, if yes then encapsulate in "***"

        authors = [
            author.strip() for author in entry.fields_dict["author"].value.split("and")
        ]
        if len(authors) > n_max_authors:
            authors = [authors[0], "et al."]

        filtered_entry = {
            "title": entry.fields_dict["title"].value,
            "authors": authors,
            "journal": null_checker(entry, "journal"),
            "doi": null_checker(entry, "doi"),
            "url": null_checker(entry, "url"),
        }

        year = entry.fields_dict.get("year").value
        month = (
            entry.fields_dict.get("month").value.lower()
            if "month" in entry.fields_dict
            else None
        )

        if year:
            full_date = str(year)
            if month:
                full_date = f"{year}-{months_to_num_dict[month]:02d}"

        filtered_entry["date"] = full_date

        new_output.append(
            {key: value for key, value in filtered_entry.items() if value is not None}
        )

    with open(output_file, "w") as yaml_file:
        yaml.dump(new_output, yaml_file, sort_keys=False)

    print(f"Filtered entries have been written to {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Tool to convert BibTeX bibliography to a YAML file"
    )
    parser.add_argument(
        "-i", "--input-file", type=str, help="Input file path", default="pubs.bib"
    )
    parser.add_argument(
        "-o",
        "--output-file",
        type=str,
        help="Output file path, optional",
        default="pubs.yml",
    )
    parser.add_argument(
        "-n",
        "--n-max-authors",
        type=int,
        help="Max number of authors to display, When higher than this treshold, only the first author is shown, the rest is displayed as 'et al'",
        default=7,
    )

    args = parser.parse_args()

    convert_bib(args.input_file, args.output_file, args.n_max_authors)


if __name__ == "__main__":
    main()
