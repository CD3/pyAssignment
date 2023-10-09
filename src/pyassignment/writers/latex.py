import random
import string

from pylatex import (Command, Document, Enumerate, Figure, Foot, Head, Itemize,
                     MiniPage, Package, PageStyle)
from pylatex.section import Paragraph, Section
from pylatex.utils import NoEscape, italic

from ..utils import collection
from .writer_base import WriterBase


class Latex(WriterBase):
    """
    Customization Points:

    assignment.meta.title : document title.
    assignment.meta.date : document date.
    assignment.meta.header : dict of fancy headers.
    assignment.meta.footer : dict of fancy footers.
    assignment.meta.make_key : bool that specifies if a key should be printed at the end of the document.
    assignment.meta.header_includes : list of lines that will be added to the preamble.
    assignment.meta.latex_packages: list of latex packages that will be loaded with '\\usepackage'
    assignment.meta.latex_preamble_lines: list of lines that will be added to the preamble.
    assignment.meta.config['questions']['enumeration_symbols'] : list of symbols used for question numbering.
    assignment.meta.config['answer']['multiple/choice_symbol'] : symbol used for multiple choice answers.
    assignment.meta.config['answer']['numerical/spacing'] : spacing added after a question with a numerical answer.
    assignment.meta.config['answer']['text/spacing'] : spacing added after a question with a text answer.
    assignment.meta.randomize_multiple_choice : randomize multiple choice answers displayed under question.

    question.meta.pre_vspace : verticle space to pace before question/part text
    question.meta.post_vspace : verticle space to pace after question/part text
    question.meta.newline: if true, put question/part on new page
    question.meta.points: if set, a label indicating the number of points will be added to the question text.

    """

    def __init__(self, fh=None):
        super().__init__(fh)
        self._packages = collection()
        self._packages += "physics"
        self._packages += "siunitx"
        self._packages += "fullpage"
        self._packages += "datetime"

        self.make_key = False

    @property
    def packages(self):
        return self._packages

    @packages.setter
    def packages(self, val):
        self._packages = val

    def dump(self, ass, fh=None):
        fh = super().get_fh(fh)

        doc = Document()

        self.build_preamble(doc, ass)
        self.build_questions(doc, ass)
        self.build_figures(doc, ass)

        make_key = self.make_key
        # if assignment has a make_key entry, use it instead
        if ass.meta.has("make_key"):
            make_key = ass.meta.make_key
        if make_key:
            self.build_key(doc, ass)

        fh.write(doc.dumps())

        return

    # we have to overwrite base class functions for getting the multiple choice
    # answer texts so we can get and return the id for each answer so that we
    # can create a \label/\ref pair
    def MC_Answer_get_all_choices(self, a):
        all_choices = list()
        salt = str(id(a))

        for i in range(len(a._choices)):
            ans_id = id(a._choices[i])
            ans_text = a._formatter.fmt(a._choices[i], **a.NS.__dict__)
            all_choices.append((salt + "-" + str(ans_id), ans_text))

        # we want to allow the answer to override the add_none_of_the_above_choice
        # configuration option
        add_none_of_the_above_choice = self.config.add_none_of_the_above_choice
        if a.meta.has("add_none_of_the_above_choice"):
            add_none_of_the_above_choice = a.meta.add_none_of_the_above_choice

        none_of_the_above_text = self.config.none_of_the_above_text
        if a.meta.has("none_of_the_above_text"):
            none_of_the_above_text = a.meta.none_of_the_above_text

        if add_none_of_the_above_choice:
            all_choices += [(salt + "-1", none_of_the_above_text)]

        return all_choices

    def MC_Answer_get_correct_choices(self, a):
        all_choices = self.MC_Answer_get_all_choices(a)
        correct_choices = list()

        if len(a._correct) == 0:
            correct_choices.append(all_choices[-1])
        for i in a._correct:
            correct_choices.append(all_choices[i])

        return correct_choices

    def build_answer(self, config, doc, q):
        if q._answer is not None:
            try:  # multiple choice
                # NOTE: need to access all_formatted_choices member of q._answer
                # so that try block will fail before an enumeration is created
                all_choices = self.MC_Answer_get_all_choices(q._answer)
                symb = r"\alph*)"
                try:
                    symb = config["answer"]["multiple_choice/symbol"]
                except:
                    pass
                doc.append(NoEscape(r" \\ "))
                with doc.create(MiniPage()):
                    with doc.create(
                        Enumerate(enumeration_symbol=NoEscape(symb))
                    ) as clist:
                        for choice in all_choices:
                            label = r"\label{%s}" % choice[0]
                            clist.add_item(NoEscape(label + choice[1]))
            except:
                pass

            try:  # numerical
                ans = q._answer.quantity
                space = "2in"
                try:
                    space = config["answer"]["numerical/spacing"]
                except:
                    pass
                doc.append(NoEscape(r"\vspace{%s}" % space))
            except:
                pass

            try:  # text
                ans = q._answer.text
                space = "2in"
                try:
                    space = config["answer"]["text/spacing"]
                except:
                    pass
                doc.append(NoEscape(r"\vspace{%s}" % space))
            except:
                pass

    def get_counter_for_level(self, i):
        if i == 0:
            return "enumi"
        if i == 1:
            return "enumii"
        if i == 2:
            return "enumiii"
        if i == 3:
            return "enumiv"

    def build_question(self, config, doc, q, i, enum_symbs, level):
        label = r"\label{%s}" % q._uuid
        if q.meta.has("label"):
            label += r"\label{%s}" % q.meta.label

        # start text for question
        text = label

        # add points indicator if given
        if q.meta.has("points") and int(q.meta.points) > 0:
            if int(q.meta.points) == 1:
                text += f"({q.meta.points} point) "
            else:
                text += f"({q.meta.points} points) "

        if len(q._figures) > 0:
            if len(q._figures) > 1:
                raise RuntimeError(
                    "WARNING: multiple figures detected in a single question. This is not supported by the LaTeX Writer.\n"
                )
            f = q._figures[0]
            text += r"For this question, consider Figure \ref{%s}. " % f._uuid
        text += q.formatted_text

        if q.meta.has("newpage") and q.meta.newpage:
            doc.append(Command("newpage"))

        if q.meta.has("pre_vspace"):
            doc.append(Command("vspace", q.meta.pre_vspace))

        with doc.create(
            Enumerate(enumeration_symbol=NoEscape(enum_symbs[level]))
        ) as qlist:
            doc.append(Command("setcounter", [self.get_counter_for_level(level), i]))

            qlist.add_item(NoEscape(text))
            self.build_answer(config, doc, q)

            if q.meta.has("post_vspace"):
                doc.append(Command("vspace", q.meta.post_vspace))

            for j in range(len(q._parts)):
                p = q._parts[j]
                self.build_question(config, doc, p, j, enum_symbs, level + 1)

    def build_questions(self, doc, ass):
        enumeration_symbols = list()
        if ass.meta.has("config"):
            if (
                ass.meta.config.get("questions", dict()).get(
                    "enumeration_symbols", None
                )
                is not None
            ):
                for symb in ass.meta.config["questions"]["enumeration_symbols"]:
                    enumeration_symbols.append(symb)

        while len(enumeration_symbols) < 5:
            enumeration_symbols.append(r"\arabic*.")

        if -1 in ass._information:
            doc.append(NoEscape(ass._information[-1].formatted_text))
            doc.append(NoEscape(""))

        level = 0
        for i in range(len(ass._questions)):
            if i in ass._information:
                doc.append(NoEscape(ass._information[i].formatted_text))

            q = ass._questions[i]
            self.build_question(ass.meta.config, doc, q, i, enumeration_symbols, level)

    def build_preamble(self, doc, ass):
        # add packages
        for e in self._packages + ass.meta.__dict__.get("latex_packages", list()):
            try:
                p, o = e
            except:
                p = e
                o = None

            doc.preamble.append(Package(p, o))

        # allow assignment metadata to add header info
        # this allows support pandoc-style config data in input files
        if ass.meta.has("header_includes"):
            if not isinstance(ass.meta.header_includes, list):
                ass.meta.header_includes = [ass.meta.header_includes]
            for line in ass.meta.header_includes:
                doc.preamble.append(NoEscape(line))

        # allow assignment metadata to add header info
        if ass.meta.has("latex_preamble_lines"):
            if not isinstance(ass.meta.latex_preamble_lines, list):
                ass.meta.latex_preamble_lines = [ass.meta.latex_preamble_lines]
            for line in ass.meta.latex_preamble_lines:
                doc.preamble.append(NoEscape(line))

        doc.preamble.append(Package("fancyhdr"))
        doc.preamble.append(Command("pagestyle", "fancyplain"))
        doc.preamble.append(Command("setlength", [NoEscape(r"\headheight"), "0.5in"]))
        if ass.meta.has("header"):
            for h in ass.meta.header:
                doc.preamble.append(Head(position=h, data=NoEscape(ass.meta.header[h])))
        if ass.meta.has("footer"):
            for f in ass.meta.footer:
                doc.preamble.append(Foot(position=f, data=NoEscape(ass.meta.footer[f])))
        doc.preamble.append(
            Command("renewcommand", [NoEscape(r"\headrulewidth"), "0pt"])
        )

        maketitle = False
        if ass.meta.has("title"):
            doc.preamble.append(Command("title", ass.meta.title))
            maketitle = True
        if ass.meta.has("date"):
            doc.preamble.append(Command("date", ass.meta.date))
            maketitle = True
        else:
            doc.preamble.append(Command("date", ""))

        doc.preamble.append(Command("setlength", [NoEscape(r"\parindent"), "0in"]))

        if maketitle:
            doc.append(NoEscape(r"\maketitle"))

    def build_figures(self, doc, ass):
        figures = (
            ass._figures
            + [f for q in ass._questions for f in q._figures]
            + [f for q in ass._questions for p in q._parts for f in p._figures]
        )
        for f in figures:
            with doc.create(Figure()) as fig:
                width = r"0.4\textwidth"
                if f.meta.has("width"):
                    width = f.meta.width
                fig.add_image(f.filename, width=NoEscape(width))
                label = r"\label{%s}" % f._uuid
                if f.meta.has("label"):
                    label += r"\label{%s}" % f.meta.label
                fig.add_caption(NoEscape(label + f.formatted_caption))

    def build_key(self, doc, ass):
        doc.append(NoEscape(r"\newpage"))
        doc.append(NoEscape(r"\textbf{\large Answers:}"))

        def write_answer(q):
            if q._answer is not None:
                try:  # multiple choice
                    answers = [
                        r"\ref{%s}" % choice[0]
                        for choice in self.MC_Answer_get_correct_choices(q._answer)
                    ]

                    doc.append(NoEscape(",".join(answers)))
                except:
                    pass

                try:  # numerical
                    ans = q._answer.quantity
                    doc.append(NoEscape("{}".format(ans)))
                except:
                    pass

                try:  # text
                    ans = q._answer.text
                    doc.append(NoEscape("{}".format(ans)))
                except:
                    pass

        for i in range(len(ass._questions)):
            q = ass._questions[i]
            doc.append(NoEscape(r"\\ \ref{%s} " % q._uuid))
            write_answer(q)

            for j in range(len(q._parts)):
                p = q._parts[j]
                doc.append(NoEscape(r"\\ \ref{%s}\ref{%s} " % (q._uuid, p._uuid)))
                write_answer(p)
