"mergefonts Help\n",
"============\n",
"mergefonts [-cid cidfontinfo file ] [-hints] output-font-file [[glyph alias file] merge-font-file]+\n",
"mergefonts  [-u] [-h]\n",
" \n",
"This tool is based on the tx program.  If the output file mode (e.g -cff, -t1,\n",
"etc) specified, then it will behave exactly as does tx. Run the command 'tx -u\n",
"for these options, and 'tx -h' for details..\n",
"  \n",
" This tool will merge one or more fonts into a parent font. The new output font\n",
" will be the same format as the first input font. The first font path in the argument\n",
" list is  the output file path.  Subsequent arguments are pairs of glyph alias\n",
" files and source fonts. The first source font  is used as the parent font; this\n",
" means that all global data for the output font is inherited from this font.\n",
"\n",
" The glyph alias file for any source font may be omitted. If present, it will be\n",
" used to both restrict the merged glyphs to those named in the source list, and\n",
" to rename the glyphs. If the FontName and Language group fields are included in\n",
" the header line of the GA file , they will override the values of the same\n",
" names on the first source font PostScript  FontDict. If the glyph alias  file for\n",
" a source font is not provided, all glyphs from the source font will be copied\n",
" through  without modification.\n",
"\n",
"The first line of a glyph alias file is a header line, and must begin with\n",
"'mergefonts'; if not, the program will attempt to parse it as a font. The\n",
"program name may be followed  by optional fields for the PostScript name and\n",
"Language group values. If present, both must be present. Each subsequent line\n",
"must consist of a pair of glyph names: the source font glyph name in the right\n",
"column, the output font glyph name in the left column.  The file must have a\n",
"final new-line.\n",
"\n",
"Example:\n",
"--------------------------------------------\n",
"mergefonts LogocistStd-Medium 0\n",
"0    .notdef\n",
"1    space\n",
"--------------------------------------------\n",
" \n",
"Note that if the  glyph alias files map glyph names to numeric values, the\n",
"mergefonts program will write the output font as a CID font, independent of\n",
"whether the source fonts are CID-keyed or not.\n",
"\n",
"Note that the final output font must contain a .notdef; if glyph alias files are\n",
"used for all the source  fonts, at least one must contain a mapping for the\n",
".notdef glyph.\n",
"\n",
"If the output font is a CID-keyed font, the option  '-cid <cidfontinfo>' may be\n",
"used. This option will use the key/value pairs in a text file to override the\n",
"top PostScript FontDict values. This text file must contain the following\n",
"key-words; example values are provided.\n",
"Required:\n",
"--------------------------------------------\n",
"FontName     (KozMinStd-Light)\n",
"FullName     (Kozuka Mincho Standard OpenType Light)\n",
"FamilyName   (Kozuka Mincho Standard OpenType)\n",
"Weight       (Light)\n",
"version      (4.005)\n",
"Registry     (Adobe)\n",
"Ordering     (Japan1)\n",
"Supplement   3\n",
"AdobeCopyright  (Copyright 1997 Adobe Systems Incorporated. All Rights Reserved.)\n",
"--------------------------------------------\n",
"Optional\n",
"--------------------------------------------\n",
"Trademark     (Kozuka Mincho is either a registered trademark or trademark of Adobe Systems Incorporated in the United States and/or other countries.)\n",
"XUID       1 11 9273722\n",
"--------------------------------------------\n",
"\n",
"[options]\n",
"-g <list>  glyph selector: tag, cid, or glyph name. May use ranges. Will\n",
"           subset the first source font only.\n",
"\n",
"-gx <list>  glyph exclusion selector: tag, cid, or glyph name. May use\n",
"            ranges. Will subset the first source font only. All glyphs except those\n",
"            listed are copied. The .notdef glyph will never be excluded.\n",
" \n",
"-cid <font-info path>  force the output font to be a CID-keyed font, even if\n",
"                       the parent font is name-keyed. See -h for example, and for format of\n",
"                       fontinfo file.\n",
"\n",
"-hints  This option can be used only with Type 1 fonts, and with only two\n",
"        source fonts. It copies the font global metrics and hint data from the\n",
"        first font, and the glyph data and font name from the second font.\n",
"\n",
"[other options]\n",
"-u              print usage\n",
"-h              print help\n",
"-v              print component versions\n",
"\n",
