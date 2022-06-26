#!/usr/bin/env python3
import argparse
import json
import logging
import time

# Global outputs
OUTPUT_LIST = []
JSON_OUTPUT_LIST = []

# Logging config
logging.basicConfig(level=logging.INFO, format="")
log = logging.getLogger()


def save_json(filename, json_data):
    """
    Takes specified output filename and valid JSON as input; writes to file.
    filename: string of filename to output to ("example.json").
    json_data: Valid JSON object to write to file.
    """
    with open(filename, "a") as f:
        json.dump(json_data, f, ensure_ascii=False)
        f.close()


def load_json(json_file):
    """
    Loads file containing JSON data and returns said data as object.
    json_file: string of filename to load JSON from.
    """
    try:
        with open(json_file) as f:
            data = json.load(f)
            f.close
        return data
    except Exception as e:
        log.critical(f"Unable to load {json_file} with the following error: {e}")


def homoglyph_generator(index_of_homoglyph):
    """
    Swaps and outputs all available homoglyphs for indexed character in string supplied by args.input.
    index_of_homoglyph: index of character in list where homoglyph should be swapped. Used for map()/iterable functionality.
    """
    # Note dependency on "homoglyphs.json" file packaged with script
    homoglyphs = load_json("homoglyphs.json")
    character_list = list(args.input)
    character = character_list[index_of_homoglyph]
    if character in homoglyphs.keys():
        if args.both_cases:
            try:
                homoglyph_list = (
                    homoglyphs[character.lower()] + homoglyphs[character.upper()]
                )
            except Exception as e:
                log.warning(
                    f"Error encountered with case switching for character {character}: {e}. Continuing with original case only"
                )

        else:
            homoglyph_list = homoglyphs[character]
        for homoglyph in homoglyph_list:
            if homoglyph != character:
                character_list[index_of_homoglyph] = homoglyph
                if args.verbose:
                    # See https://docs.python.org/3/howto/unicode.html#unicode-literals-in-python-source-code
                    unicode_literal = str(homoglyph.encode("unicode_escape").decode())
                    raw_output = f"{''.join(character_list)}  \t The character {character} was replaced with {homoglyph} (Unicode literal: {unicode_literal})"
                    OUTPUT_LIST.append(raw_output)
                    if args.output_json:
                        json_output = {
                            "original_input": character,
                            "homoglyph": homoglyph,
                            "output": f"{''.join(character_list)}",
                            "unicode_literal": unicode_literal,
                        }
                        JSON_OUTPUT_LIST.append(json_output)
                else:
                    raw_output = f"{''.join(character_list)}"
                    OUTPUT_LIST.append(raw_output)
                    if args.output_json:
                        json_output = {"output": f"{''.join(character_list)}"}
                        JSON_OUTPUT_LIST.append(json_output)


def output_controller(OUTPUT_LIST, JSON_OUTPUT_LIST):
    """
    Outputs homoglyph swaps to terminal/txt/json depending on presence of -oN/-oJ flags.
    OUTPUT_LIST: list containing homoglyph-swapped permutations of original string input.
    JSON_OUTPUT_LIST: json containing homoglyph-swapped permutations of original string input.
    """
    if args.output_normal:
        args.output_normal = filename_creator("txt", args.output_normal, "homoglyph-swapper")
        [log.info(line) for line in OUTPUT_LIST]
        with open(args.output_normal, "a") as f:
            [f.write(f"{line}\n") for line in OUTPUT_LIST]
            f.close()
    elif args.output_json:
        args.output_json = filename_creator("json", args.output_json, "homoglyph-swapper")
        if args.verbose:
            log.info(json.dumps(JSON_OUTPUT_LIST, indent=4, ensure_ascii=False))
            save_json(args.output_json, JSON_OUTPUT_LIST)
        else:
            json_output = {"output": OUTPUT_LIST}
            log.info(json.dumps(json_output, indent=4, ensure_ascii=False))
            save_json(args.output_json, json_output)
    else:
        [log.info(line) for line in OUTPUT_LIST]


def filename_creator(extension, output_type, modifier=""):
    """
    Creates filename based on specified inputs. Auto-creates filenames if -oJ/-oN flags are passed without arguments.
    extension: string of file extension type to output to (e.g. "txt").
    output_type: args.output_normal/args.output_json, determines/parses flag arguments if provided.
    """
    if modifier:
        modifier = f"{modifier}-"
    # To support both no-argument and argument output flags
    if output_type == " ":
        timestr = time.strftime("%Y%m%d-%H%M%S")
        output_type = f"{modifier}{timestr}.{extension}"
        return output_type
    else:
        return output_type


if __name__ == "__main__":
    # Parse command line
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--input",
        help="Accepts either a string as input (e.g. 'john.smith@example.com')",
        required="True",
        action="store",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="Verbose output includes referencing of swapped character, homoglyph used for swapping \
        and UTF string literal of homoglyph",
        action="store_true",
    )
    parser.add_argument(
        "-oJ",
        "--output_json",
        help="Output JSON-formatted results to (optionally specified) file (defaults to homoglyph-swapper-YYYYMMDD-HHMMSS.json)",
        action="store",
        nargs="?",
        const=" ",
    )
    parser.add_argument(
        "-oN",
        "--output_normal",
        help="Output normal-formatted results to (optionally specified) file (defaults to homoglyph-swapper-YYYYMMDD-HHMMSS.txt)",
        action="store",
        nargs="?",
        const=" ",
    )
    parser.add_argument(
        "-c",
        "--both_cases",
        help="Substitute character with both uppercase and lowercase homoglyphs where available",
        action="store_true",
    )

    args = parser.parse_args()
    list(map(homoglyph_generator, list(range(len(args.input)))))
    output_controller(OUTPUT_LIST, JSON_OUTPUT_LIST)
