# The failures these rules came from

*Cleaned copy, 15 October 2026, of a working document in the xAI investigation's notes vault (written 12 September to 4 October 2026). Names of people, companies and specific agency files are generalized. Every number about the process is unchanged.*

> [!IMPORTANT] Why this file exists
> The investigation's skill (Claude's standing instructions for this project) used to carry a rule **and** the full story of the day it was written, which roughly doubled its length. The skill now carries the rule plus a one-clause reason and a pointer here. **The reasoning is not optional** - the skill's own principle is that *a rule without its reasoning cannot be applied to a case its author did not foresee*. This is where the reasoning lives, in the vault, searchable and maintainable.
>
> **If you are about to argue that one of these rules is over-cautious, read its entry first.**

## Re-deriving work that already existed - seven sessions

**The count is seven.** Do not carry a second figure anywhere else.

- **27 August 2026.** A session was handed two jobs marked *blocking*. Both were already finished - a permit's monitoring reports on 5 August, a securities filing on 29 July. `_check.py` on the permit number returns **158 notes** and would have stopped both. Nobody ran it because it did not exist yet. Both false jobs came from Notion rows written by earlier sessions that had not searched `Documents/` first; the rows then read as authority and the next session's brief inherited them. **This is why a board row, and anything in a session brief, is a claim and not a fact.**
- **5 September 2026, the seventh and the different one.** A compacted session rebuilt an exhibit that had already been finished the previous evening, from the base image Rachel had *rejected*, and reported it to her twice as new work. One `git log` would have caught it. **Every other gate fires before research. None of them fires when a session resumes mid-task believing it already knows the state.** That is what the resume-time check (STEP ZERO-A) is for.
- **The district-line work** existed from 27 July 2026 as a PNG and four Python scripts, and was re-derived because **anything that is only pixels is invisible to search.**

## Coverage claims written from feel

- **27 August 2026.** A planning document (a series running order) said *"Everything in the vault has been read."* The computed figure was **236 of 1,806 verified, 13.1 percent**. Nobody lied; a session wrote a coverage claim from feel instead of from a count. **Hence: coverage is generated, never written.**
- **27 August 2026.** There were **241 notes in `Documents/` with no read tag at all** - 241 documents nobody could prove were read without reading them again. **Hence: an untagged read did not happen.**
- **A first draft of `_tag.py` invented a stricter tag format** and declared 545 correctly tagged notes malformed. **Hence: do not hand-write the tag string and do not invent a format.**

## Universal negatives with a swapped scope

**27 August 2026.** The same running order said a signer's *"name appears nowhere else in 1,705 files."* `_check.py` on the signer's name returns **34 notes, 58 lines**, including a tested row already in `+ANSWERED`. The underlying finding had said "nowhere else *in it*" - meaning one permit collection. **The narrative kept the sentence and swapped the scope.** It was going to be the lede of a piece about a named person.

## A checker that credits its own output

**27 August 2026.** `_close.py` wrote un-noted filenames into `+READ MANIFEST`, then walked that file on the next run and counted them as covered. The known symptom was "the second consecutive run lies." It was worse: **the credit persisted across sessions**, so any name that ever landed in the manifest counted as covered forever. It reported 1,860 of 1,872 files covered when the true figure was **1,212**. Fixed 27 August 2026.

**The general lesson, which outlives the bug:** when a checker reads anything it also writes, its clean report means nothing. **If anyone re-adds `+READ MANIFEST` or `Hot cache` to the scan, the coverage numbers become meaningless again.**

**Related, same day:** a marking script passed its own dry run and still stacked a duplicate callout on five files, because the dry run reported what it *meant* to do instead of the text it would write. **Make dry runs print the produced text.**

## Frontmatter that fails silently

**27 August 2026.** 43 notes carried a double-quoted frontmatter value containing its own double quotes. **Dataview does not warn - it skips the note.** The MOCs under-reported for three weeks. The YAML rule is in the skill's `references/NOTE-TYPES.md`.

## A naming problem mistaken for a duplication problem

Notes named after two companies and numbered `2` through `10`, and four notes spelling one company name four different ways, look like a mess of copies. **They are not - each is a different recorded instrument**: an easement, a lien, a quitclaim deed, a deed of trust. They carry those names because **the county Register of Deeds names its downloads after the grantor** and the browser auto-numbered the collisions.

**A merge pass would have destroyed nine distinct land records.** 39 notes were renamed instead on 27 August 2026 by `_vault_rename.py`, which repoints every wikilink and writes an undo manifest.

## Why a dedupe on the source library would destroy evidence

112 files exist in more than one place; 209 redundant copies. Deleting the extras looks like obvious housekeeping.

- Two PDFs in one agency production are **byte-identical under filenames dated seventeen days apart.** Another pair, eight weeks apart.
- **Nine of the eleven files shared between two rounds of an air-modelling submission are byte-identical**, with only two results spreadsheets actually changing.

**Both facts exist only because the copies were still there to compare.** Most redundant copies already sit in `_duplicates (safe to ignore)` and are hurting nobody.

**The rule that came out of it:** a date in an agency's permit-records filename is **not** a document date. An agency email collection carries the same defect, with filename dates running 0 to 4 days earlier than the header. Any figure resting on a filename date needs its document opened.

## Corrections that made it worse

**4 August 2026, a sibling investigation vault.** A one-word error was "corrected" twice, introducing four new wrong numbers, before a third pass restored the original figure. **A wrong correction inherits the authority of the fix, so it does more damage than the error it replaces.**

**A missing source is a sourcing question, not a factual error.** If you cannot find where a figure came from, downgrade `strength:` and log it to close. **Never overwrite a figure on that basis.** A documented-but-not-raw number is not a wrong number.

## A litigant's page pin is not a locator

**27 August 2026.** The vault carried three page pins into a securities filing, taken from the court briefs that cite it. **All three are one page low.** The real pins are each one page higher, identical across three versions of the filing. The vault's own pin for the same filing, derived from its own read, is correct.

**A brief's citation is a claim about a document, not the document.**

## The other failure modes, from the 4 August 2026 audit of a sibling investigation

1. **A subject's claim recorded as our fact.** A company's filing describing its own operations is a document about what it *said*. Ask: measurement, agency finding, or self-description?
2. **Fixed in the notes, still wrong in the artifact.** A correction that updates a finding but not the marked image, `+NUMBERS`, `+ANSWERED` or the press packet is not done. Fix the source and rebuild; editing a generated file by hand does not hold.
3. **Precision drift under paraphrase.** A regulatory mechanism becomes a stronger everyday word; a figure attached to one thing migrates to another. Each step sounds like the last. **Go back to the document, not to the previous note.**

## Tooling traps that cost hours

- **`_manifest.py` "no note" does not mean "unread."** A set-level note covering 132 air-model files reads as 131 gaps. On 2 August a session claimed 111 state agency files were unread; they had been inventoried on 29 July by a set-level note.
- **A set-level note saying "individual runs not line-audited" is a gap, not coverage.**
- **`grep -c` counts LINES, not occurrences.** A single-line HTML file reports 1 for a word appearing forty times. A zero is still a real zero, so negative greps hold; never report a non-zero count from that method as a frequency.
- **Two summarised fetches of the same securities-filing record** returned two different filing dates and two different accession numbers for one filing on 27 August 2026. **Read the source record directly.**
- **Scripts hardcode `VAULT` and scan paths.** A sibling vault inherited a stale filename that way and its orphan check silently passed for days.
- **12 September 2026:** a scripted reading-room search returned empty for a case that was definitely present. The empties were an artifact of the script. **Prove an automated search on a known positive before trusting a negative.**

## Searching one channel and summarising as though you searched all of them

**12 September 2026.** A session searched a federal agency's reading room, flagged the frequently-requested pages as unsearched, then told Rachel a control number *"has never been posted anywhere."* Rachel asked why the second channel had been skipped. **The rule named two channels and only one was searched.** The rule is the investigation's pre-request search gate.

## A reading queue that was never rebuilt, and looked full the whole time

**16 September 2026.** The overnight loop's queue, `_tools/worklist.tsv`, had not been rebuilt since
early August. It held **730 files** while the corpus grew past 2,800. **1,809 real source files could
never be drawn at all**, spread across four agency productions and 201 court filings.
**388 of them had no note of any kind.** Nothing looked wrong: the loop reported clean runs every
night, drawing from the small end of the one folder it could still see.

**The failure is that a queue reports on itself.** `--status` answers "how much of my list is left",
never "is my list the corpus". Nobody asked the second question for six weeks.

**The rule:** rebuild the worklist whenever a production lands, and compare its row count against the
corpus before trusting any statement about what is left to read. Never quote the free count as
coverage.

**Two things fixed with it.** `_worklist.py` now skips our own derived material so machine
transcription can never be handed to a reader as a source document - the test is the substring
"extracted text" anywhere in a folder name, **not a suffix**, because the first version tested
`endswith()` and missed a folder named `<agency production> extracted text (OCR, locator only)`, leaving
51 of our own OCR files sitting in the queue as unread records for two days. And the oversize hold
was regenerated across the whole corpus under Rachel's 7 September rule, 35 rows to 92, so the
giants in the newly visible folders are held back from unattended runs too.

## Agents identify, a session reads

**15-16 September 2026, and made the loop's design on 18 September.** A 6,555-page federal agency production
was mapped by 92 agents across two workflows - 916 documents with page ranges, dates, senders,
recipients, subjects and Bates numbers, plus one plain sentence on each of 328 emails - and then
read by a session. **Every identification that was spot-checked was right. No agent was asked for
significance.**

**Rachel's instruction, 16 September:** *"having the agents tell you what they are and you reading
them."*

**The division, and why it is drawn exactly there.** Finding out WHAT a file is - page boundaries,
dates, parties, which pages are images, whether a hidden form layer exists - is mechanical, parallel
and checkable against the page. Deciding what a document MEANS is neither. An agent that reports
what is significant has made the judgment, and the reading is then a formality performed over
somebody else's conclusion.

**The rule that keeps it honest: the map sets the ORDER of reading, never what gets read.** Where a
file is genuinely too long to read whole, the note says so and the tag records `--partial`, never
`--full`. A full tag on a file whose pages were picked by a map is the one output this loop must
never produce.

**Tested before it shipped, 18 September 2026.** One agent identified a six-page recorded
construction lien, image-only, no text layer. It named the instrument, both attorneys with bar
numbers, the firm, the clerk's stamp, the book and page range, and the legal description, and it
flagged its own uncertainty on a handwritten jurat which it then resolved at 450 dpi. **Two pages
were checked against the rendered page by eye and every call was right**, including a drop-cap the
OCR had read as "Norice" and a handwritten year that reads as "2b" at low resolution. It volunteered
no conclusions.

*Extracted from the skill 12 September 2026 so the skill could carry the rules and this could carry the reasons. Nothing here was invented; every entry came out of the skill as written. Two sections added 18 September 2026 from the queue rebuild and the loop redesign.*

## Moved from the Notion xAI Hub, 4 October 2026

*These two blocks sat on the investigation's Notion hub from 14 September. When the investigation moved off Notion on 4 October 2026 they were copied here word for word. The `_check.py` defect was written down nowhere else in the vault.*

### Extraction traps that have each cost real time

- **Broken CID fonts.** Roughly 30 documents return garbage from pdftotext. Use `_tools/_cidfix.py` - invert the embedded font cmap, do not reach for OCR.
- **Type 3 vector-outline PDFs** have no character mapping and must be rendered and read visually. The garbling often affects only the Outlook wrapper while the agency form underneath extracts cleanly - check the whole extraction before declaring a file unreadable.
- **A page that extracts to empty or near-empty text is an image.** Grep is blind to it, so a clean search result on a scanned production means nothing.
- **Check an xlsx dimension reference before trusting a row count.** A plain value extraction of a state agency spreadsheet silently dropped three rows, including the legend that explained the file.
- **Distinguish filing date from approval date from issuance date from portal upload stamp.** That distinction has broken a headline claim once already.
- **Identify files by content, never by filename.** An agency's own filename gave a speaker one first name; the hearing transcript, in the speaker's own words, gives another.

### The `_check.py` defect, in full

It reads every vault note inside `try: ... except OSError: continue`. A file it cannot read is silently skipped and counted as "no match." When the vault is evicted to iCloud, unreadable notes are invisible to it, and the gate cannot tell "nothing found" from "could not read it." `_audit_dupes.py`, `_audit_inventory.py`, `_claim.py` and `_batchE_markdone.py` share the pattern. Never judge a tool's output from a truncated view either - that produced a false "no xAI hits" negative from a truncated transcript.

**So a zero from `_check.py` is only meaningful when the vault is fully downloaded.** Check for evicted files first (`find . -name "*.icloud"` from the vault should print nothing).
