from manim import *
from manim.opengl import *
import numpy as np
from typing import Optional

X_MOVE = 5.5
Y_MOVE = 2
PAUSE = 0.8
OPACITY = 0.5
DEF_SCALE = 0.75
N = 2000
N_TOP = 800
N_BOT = N-N_TOP
DEN_TOP = 80
DEN_BOT = 120
CONS_TOP = 45
CONS_BOT = 45
CONS_MID = 10
TIMES = (N_TOP/DEN_TOP, CONS_TOP, CONS_BOT, N_BOT/DEN_BOT, CONS_MID)
DECS = (2, 0, 0, 2, 0)
DEF_COL = BLUE_D
TABLE_WIDTH = 10.0
TABLE_HEIGHT = 5.0

def division(n, d):
    return ['{', n, r'\over', d, '}']


class GTtable(VMobject): # zatim fixed, v budoucnu zmenit velikost v zavislosti na textu
    def __init__(self,
                 table_strs: list[list[tuple[str] | str]],
                 row_headers: Optional[list[str]] = None,
                 col_headers: Optional[list[str]] = None,
                 table_width: float = TABLE_WIDTH,
                 table_height: float = TABLE_HEIGHT,
                 n_rows: int = 2,
                 n_cols: int = 2,
                 **kwargs):
        super().__init__(**kwargs)

        self.table_strs = table_strs
        self.row_headers = row_headers
        self.col_headers = col_headers
        self.table_width = table_width
        self.table_height = table_height
        self.n_rows = n_rows
        self.n_cols = n_cols

        self.rows = [VGroup(*[Rectangle(width=table_width/(n_rows+1), height=table_height/(n_cols+1)) for cell in range(n_cols)]).arrange(buff = 0.0)]

        for i in range(n_rows-1):
            self.rows.append(self.rows[0].copy().next_to(self.rows[0+i], DOWN, buff=0.0))

        if self.row_headers:
            self.row_headers_cells = self.rows[0].copy().next_to(self.rows[0], UP, buff=0.0)

        if self.col_headers:
            self.col_headers_cells = VGroup(*[row[0] for row in self.rows]).copy().next_to(self.rows[0][0], LEFT, buff=0.0).align_to(self.rows[0][0], UP)

        self.table_frame = VGroup(*self.rows, self.row_headers_cells, self.col_headers_cells).move_to(ORIGIN)

        self._set_header_coos()
        self._set_cell_coos_and_payoffs()
        self._set_payoffs_list()

        self.row_headers_texts = [Text(text).move_to(self.header_coos[0][i]) for i, text in enumerate(row_headers)]
        self.col_headers_texts = [Text(text).move_to(self.header_coos[1][i]) for i, text in enumerate(col_headers)]

        self.add(self.table_frame, VGroup(*self.row_headers_texts, *self.col_headers_texts, *self.list_all_payoffs))

    def _set_header_coos(self):
        self.header_coos = np.empty((self.n_rows, self.n_cols), dtype=object)
        if self.row_headers_cells:
            for i, row in enumerate(self.row_headers_cells):
                self.header_coos[0][i] = row.get_center()

        if self.col_headers_cells:
            for i, col in enumerate(self.col_headers_cells):
                self.header_coos[1][i] = col.get_center()


    def _set_cell_coos_and_payoffs(self):
        self.all_payoffs = []
        self.coos = np.empty((self.n_rows, self.n_cols), dtype=object)
        self.left_coos = np.empty((self.n_rows, self.n_cols), dtype=object)
        self.rigth_coos = np.empty((self.n_rows, self.n_cols), dtype=object)
        for i, (row, row_str) in enumerate(zip(self.rows, self.table_strs)):
            row_payoffs = []
            for j, (cell, cell_strs) in enumerate(zip(row, row_str)):
                self.coos[i][j] = cell.get_center()
                self.left_coos[i][j] = cell.get_left()
                self.rigth_coos[i][j] = cell.get_right()
                self.n_payoffs = len(cell_strs)
                payoff_space = (self.rigth_coos[i][j]-self.left_coos[i][j])/(self.n_payoffs+1)
                payoffs = []
                for k, cell_str in enumerate(cell_strs, 1):
                    payoffs.append(Text(cell_str).move_to(self.left_coos[i][j] + k*payoff_space))
                row_payoffs.append(payoffs)
            self.all_payoffs.append(row_payoffs)


    def get_cell_coos(self, row: int, col: int):
        return self.coos[row][col].get_center()


    def get_payoff_coos(self, row: int, col: int):
        return([self.all_payoffs[row][col][i].get_center() for i in range(self.n_payoffs)])


    def _set_payoffs_list(self):
        self.list_all_payoffs = []
        for i in range(self.n_rows):
            for j in range(self.n_cols):
                for k in range(self.n_payoffs):
                    self.list_all_payoffs.append(self.all_payoffs[i][j][k])

    def get_payoffs(self):
        return(self.all_payoffs)


    def get_payoffs_as_list(self):
        return(self.list_all_payoffs)


    def get_row_headers(self):
        return(self.row_headers_texts)


    def get_col_headers(self):
        return(self.col_headers_texts)


class testos(Scene):
    def construct(self):
        testosos = GTtable(table_strs=[[('1', '1'), ('3', '0')], [('0', '3'), ('2', '2')]],
                 row_headers=['Fight', 'Share'],
                 col_headers=['Fight', 'Share'],
                 table_width = TABLE_WIDTH,
                 table_height = TABLE_HEIGHT,
                 n_rows = 2,
                 n_cols = 2)
        testosos.shift(UP)
        testosos.get_payoffs()
        self.play(FadeIn(testosos.table_frame))
        self.play(FadeIn(testosos.get_payoffs()))
        self.play(FadeIn(*testosos.get_payoffs()))
        self.play(FadeIn(*testosos.get_row_headers()))
        self.play(FadeIn(*testosos.get_col_headers()))



########################################################################
# table_strs=[[('0', '01'), ('1', '10')], [('2', '02'), ('3', '30')]]
# row_headers=['a', 'b']
# col_headers=['c', 'd']
# table_width = TABLE_WIDTH
# table_height = TABLE_HEIGHT
# n_rows = 2
# n_cols = 2

# rows = [VGroup(*[Rectangle(width=table_width/(n_rows+1), height=table_height/(n_cols+1)) for cell in range(n_cols)]).arrange(buff = 0.0)]

# for i in range(n_rows-1):
#     rows.append(rows[0].copy().next_to(rows[0+i], DOWN, buff=0.0))

# row_headers_cells = rows[0].copy().next_to(rows[0], UP, buff=0.0)
# col_headers_cells = VGroup(*[row[0] for row in rows]).copy().next_to(rows[0][0], LEFT, buff=0.0).align_to(rows[0][0], UP)

# table_body = VGroup(*rows, row_headers_cells, col_headers_cells).move_to(ORIGIN)

# header_coos = np.empty((n_rows, n_cols), dtype=object)
# for i, row in enumerate(row_headers_cells):
#     header_coos[0][i] = row.get_center()

# for i, col in enumerate(col_headers_cells):
#     header_coos[1][i] = col.get_center()

# row_headers_texts = [Text(text).move_to(header_coos[0][i]) for i, text in enumerate(row_headers)]
# col_headers_texts = [Text(text).move_to(header_coos[1][i]) for i, text in enumerate(col_headers)]

# texts = []
# coos = np.empty((n_rows, n_cols), dtype=object)
# left_coos = np.empty((n_rows, n_cols), dtype=object)
# rigth_coos = np.empty((n_rows, n_cols), dtype=object)
# for i, (row, row_str) in enumerate(zip(rows, table_strs)):
#     for j, (cell, cell_strs) in enumerate(zip(row, row_str)):
#         coos[i][j] = cell.get_center()
#         left_coos[i][j] = cell.get_left()
#         rigth_coos[i][j] = cell.get_right()
#         cell_texts = []
#         n_payoffs = len(cell_strs)
#         payoff_space = (rigth_coos[i][j]-left_coos[i][j])/(n_payoffs+1)
#         for k, cell_str in enumerate(cell_strs, 1):
#             payoffs = []
#             payoffs.append(Text(cell_str).move_to(left_coos[i][j] + k*payoff_space))
#             cell_texts.append(tuple(*payoffs))
#         texts.append(cell_texts)

# list_all_payoffs = []
# for i in range(n_rows):
#     for j in range(n_cols):
#         for k in range(n_payoffs):
#             list_all_payoffs.append(texts[i][j][k])

# all_payoffs = []
# coos = np.empty((n_rows, n_cols), dtype=object)
# left_coos = np.empty((n_rows, n_cols), dtype=object)
# rigth_coos = np.empty((n_rows, n_cols), dtype=object)
# for i, (row, row_str) in enumerate(zip(rows, table_strs)):
#     row_payoffs = []
#     for j, (cell, cell_strs) in enumerate(zip(row, row_str)):
#         coos[i][j] = cell.get_center()
#         left_coos[i][j] = cell.get_left()
#         rigth_coos[i][j] = cell.get_right()
#         n_payoffs = len(cell_strs)
#         payoff_space = (rigth_coos[i][j]-left_coos[i][j])/(n_payoffs+1)
#         payoffs = []
#         for k, cell_str in enumerate(cell_strs, 1):
#             payoffs.append(Text(cell_str).move_to(left_coos[i][j] + k*payoff_space))
#         row_payoffs.append(payoffs)
#     all_payoffs.append(row_payoffs)

# list_all_payoffs = []
# for i in range(n_rows):
#     for j in range(n_cols):
#         for k in range(n_payoffs):
#             list_all_payoffs.append(all_payoffs[i][j][k])



# [r'{ {{N_a}}', ' \over ', '{{80}} }', ' = ', '{ {{N_d}}', ' \over ', '{{120}} }']
class CreateHD(Scene):
    def construct(self):
        calcs = [['EV_H = EV_D'],
                 [r'{{H}} \big( {V \over 2} - { C \over 2 } \big) + DV', '{{=}}', r'0 + { {{D}} \over 2 }'],
                 [r'{{H}} {{V}} {{- HC}} + DV', '{{=}}', '{{-D}} {{V}}'],
                 [r'{{H}} {{V}} {{- HC}}', '{{=}}', '-D {{V}}'],
                 [r'{{H}} {{V}} {{- HC}}', '{{=}}', '-(1-H) {{V}}'],
                 [r'{{H}} {{V}} {{- HC}}', '{{=}}', 'HV-{{V}}'],
                 [r'{{- HC}}', '{{=}}', '-{{V}}'],
                 [r'{{HC}}', '{{=}}', '{{V}}'],
                 [r'H ', '{{=}}', '{V \over C}']]
        
        conds = ([r'V > C'],
                 [r'V < C'],
                 [r'H > \frac{V}{C}'],
                 [r'H < \frac{V}{C}'])
        
        # headers
        
        t = GTtable(table_strs=[[('1', '1'), ('3', '0')], [('0', '3'), ('2', '2')]],
                 row_headers=['Fight', 'Share'],
                 col_headers=['Fight', 'Share'],
                 table_width = TABLE_WIDTH,
                 table_height = TABLE_HEIGHT,
                 n_rows = 2,
                 n_cols = 2)
        t.shift(UP)
        payoffs = t.get_payoffs()
        row_headers = t.get_row_headers()
        col_headers = t.get_col_headers()
        recall_prisoners_dilemma = Text('Let\'s recall prisoner\'s dilemma.')
        cooperation_and_altruism = Text('Cooperation and altruism').to_edge(UL)

        text_below_table = Text('Once again, Prisoner\'s dilemma is \"a reason why we can\'t have nice things.\"', font_size=28).next_to(t.get_bottom(), DOWN).shift(DOWN)


        self.play(Write(recall_prisoners_dilemma))
        self.play(FadeOut(recall_prisoners_dilemma))
        self.play(FadeIn(t.table_frame))

        self.play(AnimationGroup(Write(row_headers[0]), Write(row_headers[1])))
        self.play(AnimationGroup(Write(col_headers[0]), Write(col_headers[1])))
        
        self.play(FadeIn(VGroup(*payoffs[0][0])))
        self.play(FadeIn(VGroup(*payoffs[0][1])))
        self.play(FadeIn(VGroup(*payoffs[1][0])))
        self.play(FadeIn(VGroup(*payoffs[1][1])))

        self.play(Indicate(VGroup(payoffs[0][0][0], payoffs[0][1][0])))
        self.play(Indicate(VGroup(payoffs[0][0][1], payoffs[1][0][1])))
        self.wait()
        self.play(Write(text_below_table))
        self.play(FadeOut(VGroup(t, text_below_table)))
        self.play(Write(cooperation_and_altruism))
        
        
        t = Table([['', ''],
                   ['', '']],
                  row_labels=[Text('Hawk meets'), Text('Dove meets')],
                  col_labels=[Text('Hawk'), Text('Dove')],
                  include_outer_lines=True).shift(UP)

        cells = []
        for i in range(2, 4):
            for j in range(2, 4):
                cells.append(t.get_cell((i,j)).get_center())
        
        vals = t.get_entries()
        vals.set_opacity(0)
        labs = t.get_labels()
        self.play(FadeIn(t))

        for lab in labs:
            self.play(lab.animate.set_opacity(1))
        
        value = MathTex('{{V}}').save_state()
        cost = MathTex('{{C}}').save_state()
        hawks = MathTex('{{H}}').save_state()
        doves = MathTex('{{D}}').save_state()
        value_desc = MathTex(r'\text{--- Value or payoff}').save_state()
        cost_desc = MathTex(r'\text{--- Cost}').save_state()
        hawks_desc = MathTex(r'\text{--- The proportion of hawks}').save_state()
        doves_desc = MathTex(r'\text{--- The proportion of doves}').save_state()
        one_minus_hawks = MathTex('1 - H').save_state()
        
        value_desc.next_to(t, DOWN)
        value.next_to(value_desc, LEFT)
        cost.next_to(value, DOWN)
        cost_desc.next_to(cost, RIGHT)
        
        fight = MathTex('{', *division('{{V}}', '2'), '-', *division('{{C}}', '2'), '}').move_to(cells[0])
        share = MathTex(*division('{{V}}', '2')).move_to(cells[3])
        # fight = MathTex('{', '{', '{{V}}', r'\over', '2', '}', '-', '{', '{{C}}', r'\over', '2', '}', '}').move_to(cells[0])
        
        self.play(Create(VGroup(value, value_desc)))
        self.play(Create(VGroup(cost, cost_desc)))

        self.play(TransformMatchingTex(VGroup(value.copy(), cost.copy()), fight))
        self.play(value.copy().animate.move_to(cells[1]))
        self.play(FadeIn(MathTex('0').move_to(cells[2])))
        self.play(TransformMatchingTex(value.copy(), share))

        calc_eqs = []
        for i, calc in enumerate(calcs):
            self.wait()
            calc_eqs.append(MathTex(*calc).scale(DEF_SCALE).move_to([-4,3,0]))
            if i == 0:
                self.play(Create(*calc_eqs[i]))
            else:
                calc_eqs[i].next_to(calc_eqs[i-1], DOWN)
                self.play(TransformMatchingTex(calc_eqs[i-1].copy(), calc_eqs[i]))
                # self.play(TransformMatchingShapes(*calc_eqs[i:i+2]))
        

        self.wait(PAUSE)