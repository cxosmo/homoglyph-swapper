`homoglyph-swapper.py` is a tool for generating homoglyph permutations of a string input to support testing/fuzzing for [Unicode equivalence/normalisation issues](https://book.hacktricks.xyz/pentesting-web/unicode-normalization-vulnerability). The script uses homoglyph data defined in `homoglyphs.json`, which itself is derived from [codebox's homoglyph repository](https://github.com/codebox/homoglyph/blob/master/raw_data/chars.txt) and the [now-archived homoglyphs Python package](https://github.com/life4/homoglyphs).

## Disclaimer
_Printing of Unicode characters can be handled inconsistently depending on environmental factors (i.e. operating system/locale settings). Use the_ `--verbose` _flag to include raw Unicode string literal of the substituted character._

## Thanks
Thanks to [codebox](https://github.com/codebox) and [orsinium](https://github.com/orsinium) for their open-source efforts from which this tool is derived.

## Contributions
If you'd like to make any contributions or recommendations (e.g. adding to homoglyph source file or code improvements), feel free to submit a pull request/file an issue!
