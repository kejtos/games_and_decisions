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


class GTtable(VGroup): # zatim fixed, v budoucnu zmenit velikost v zavislosti na textu
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

        if self.col_headers:
            self.col_headers_cells = self.rows[0].copy().next_to(self.rows[0], UP, buff=0.0)

        if self.row_headers:
            self.row_headers_cells = VGroup(*[row[0] for row in self.rows]).copy().next_to(self.rows[0][0], LEFT, buff=0.0).align_to(self.rows[0][0], UP)

        self.frame = VGroup(*self.rows, self.col_headers_cells, self.row_headers_cells).move_to(ORIGIN)

        self._set_header_coos()
        self._set_cell_coos()
        self._set_payoffs()
        self._set_payoffs_list()
        self._set_header_texts()

        self.add(self.frame, VGroup(*self.row_headers_texts, *self.col_headers_texts, *self.list_all_payoffs))


    def _set_header_coos(self):
        self.header_coos = np.empty((self.n_rows, self.n_cols), dtype=object)
        if self.row_headers:
            for i, row in enumerate(self.row_headers_cells):
                self.header_coos[0][i] = row.get_center()

        if self.col_headers:
            for i, col in enumerate(self.col_headers_cells):
                self.header_coos[1][i] = col.get_center()


    def _set_cell_coos(self):
        self.coos = np.empty((self.n_rows, self.n_cols), dtype=object)
        self.left_coos = np.empty((self.n_rows, self.n_cols), dtype=object)
        self.rigth_coos = np.empty((self.n_rows, self.n_cols), dtype=object)
        for i, row in enumerate(self.rows):
            for j, cell in enumerate(row):
                self.coos[i][j] = cell.get_center()
                self.left_coos[i][j] = cell.get_left()
                self.rigth_coos[i][j] = cell.get_right()


    def _set_payoffs(self):
        self.all_payoffs = []
        for i, row_str in enumerate(self.table_strs):
            row_payoffs = []
            for j, input_payoffs in enumerate(row_str):
                payoffs = []
                if type(input_payoffs) in (list, tuple):
                    self.n_payoffs = len(input_payoffs)
                    payoff_space = (self.rigth_coos[i][j]-self.left_coos[i][j])/(self.n_payoffs+1)
                    for k, payoff in enumerate(input_payoffs, 1):
                        if isinstance(payoff, str):
                            payoff = Text(payoff)
                        payoffs.append(payoff.move_to(self.left_coos[i][j] + k*payoff_space))
                else:
                    self.n_payoffs = 1
                    payoff_space = (self.rigth_coos[i][j]-self.left_coos[i][j])/(self.n_payoffs+1)
                    if isinstance(input_payoffs, str):
                        payoff = Text(payoff)
                    payoffs.append(input_payoffs.move_to(self.left_coos[i][j] + payoff_space))
                row_payoffs.append(payoffs)
            self.all_payoffs.append(row_payoffs)


    def _set_payoffs_list(self):
        self.list_all_payoffs = []
        for i in range(self.n_rows):
            for j in range(self.n_cols):
                for k in range(self.n_payoffs):
                    self.list_all_payoffs.append(self.all_payoffs[i][j][k])


    def _set_header_texts(self):
        self.row_headers_texts = [Text(header).move_to(self.header_coos[0][i]) for i, header in enumerate(self.row_headers)]
        self.col_headers_texts = [Text(header).move_to(self.header_coos[1][i]) for i, header in enumerate(self.col_headers)]


    def _update_coos(self):
        self._set_header_coos()
        self._set_cell_coos()
        self._set_payoffs_list()


    def move_to(self, new_center):
        super().move_to(new_center)
        self._update_coos()
        return self


    def shift(self, *args, **kwargs):
        super().shift(*args, **kwargs)
        self._update_coos()
        return self


    def scale(self, *args, **kwargs):
        super().scale(*args, **kwargs)
        self._update_coos()
        return self


    def get_cell_coos(self, row: int, col: int):
        return self.coos[row][col]


    def get_payoff_coos(self, row: int, col: int):
        return([self.all_payoffs[row][col][i].get_center() for i in range(self.n_payoffs)])


    def get_payoffs(self):
        return(self.all_payoffs)


    def get_payoffs_as_list(self):
        return(self.list_all_payoffs)


    def get_row_headers(self):
        return(self.row_headers_texts)


    def get_col_headers(self):
        return(self.col_headers_texts)


    def update_header(self, row_col: str, pos: int, new_header: str):
        if row_col.lower() in ('row', 'rows', 'r'):
            self.row_headers_texts[pos].become(Text(new_header).move_to(self.row_headers_texts[pos]))
            self.row_headers_texts[pos] = Text(new_header).move_to(self.row_headers_texts[pos])

        if row_col.lower() in ('col', 'cols', 'c'):
            self.col_headers_texts[pos].become(Text(new_header).move_to(self.col_headers_texts[pos]))
            self.col_headers_texts[pos] = Text(new_header).move_to(self.col_headers_texts[pos])


    def update_payoff(self, row: int, col: int, pos: int, new_payoff: str | Mobject):
        if isinstance(new_payoff, str):
            new_payoff = Text(new_payoff)
        self.all_payoffs[row][col][pos].become(new_payoff.move_to(self.all_payoffs[row][col][pos]))
        self.all_payoffs[row][col][pos] = new_payoff.move_to(self.all_payoffs[row][col][pos])

# n_cols = 2
# n_rows = 2
# rows = [VGroup(*[Rectangle(width=TABLE_WIDTH/(n_rows+1), height=TABLE_HEIGHT/(n_cols+1)) for cell in range(n_cols)]).arrange(buff = 0.0)]

# for i in range(n_rows-1):
#     rows.append(rows[0].copy().next_to(rows[0+i], DOWN, buff=0.0))

# coos = np.empty((n_rows, n_cols), dtype=object)
# left_coos = np.empty((n_rows, n_cols), dtype=object)
# rigth_coos = np.empty((n_rows, n_cols), dtype=object)
# for i, row in enumerate(rows):
#     for j, cell in enumerate(row):
#         coos[i][j] = cell.get_center()
#         left_coos[i][j] = cell.get_left()
#         rigth_coos[i][j] = cell.get_right()


# all_payoffs = []
# for i, row_str in enumerate(table_strs):
#     row_payoffs = []
#     for j, input_payoffs in enumerate(row_str):
#         n_payoffs = len(input_payoffs)
#         payoff_space = (rigth_coos[i][j]-left_coos[i][j])/(n_payoffs+1)
#         payoffs = []
#         if type(input_payoffs) in (list, tuple):
#             for k, payoff in enumerate(input_payoffs, 1):
#                 if isinstance(payoff, str):
#                     payoff = Text(payoff)
#                 payoffs.append(payoff.move_to(left_coos[i][j] + k*payoff_space))
#         else:
#             if isinstance(input_payoffs, str):
#                 payoff = Text(payoff)
#             payoffs.append(input_payoffs.move_to(left_coos[i][j] + payoff_space))
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
                 [r'H', '{{=}}', '{V \over C}']]
        
        conds = ([r'V > C'],
                 [r'V < C'],
                 [r'H > \frac{V}{C}'],
                 [r'H < \frac{V}{C}'])
        
        # headers
        
        t1 = GTtable(table_strs=[[('1', '1'), ('3', '0')], [('0', '3'), ('2', '2')]],
                    row_headers=['Fight', 'Share'],
                    col_headers=['Fight', 'Share'],
                    table_width = TABLE_WIDTH,
                    table_height = TABLE_HEIGHT,
                    n_rows = 2,
                    n_cols = 2).shift(UP)

        t1.get_cell_coos(0,0)

        payoffs = t1.get_payoffs()
        row_headers = t1.get_row_headers()
        col_headers = t1.get_col_headers()
        recall_prisoners_dilemma = Text('Let\'s recall prisoner\'s dilemma.')
        cooperation_and_altruism = Text('Cooperation and altruism').to_edge(UL)

        text_below_table = Text('Once again, Prisoner\'s dilemma is \"a reason why we can\'t have nice things.\"', font_size=28).next_to(t1.frame.get_bottom(), DOWN).shift(DOWN)

        self.play(Write(recall_prisoners_dilemma))
        self.play(FadeOut(recall_prisoners_dilemma))
        self.play(FadeIn(t1.frame))

        self.play(AnimationGroup(Write(row_headers[0]), Write(row_headers[1])))
        self.play(AnimationGroup(Write(col_headers[0]), Write(col_headers[1])))
        
        self.play(FadeIn(VGroup(*payoffs[0][0])))
        self.play(FadeIn(VGroup(*payoffs[0][1])))
        self.play(FadeIn(VGroup(*payoffs[1][0])))
        self.play(FadeIn(VGroup(*payoffs[1][1])))

        self.play(Indicate(VGroup(payoffs[0][0][0], payoffs[0][1][0])))
        self.play(Indicate(VGroup(payoffs[0][0][1], payoffs[1][0][1])))
        self.play(Indicate(VGroup(payoffs[0][0][0], payoffs[0][0][1])))

        self.play(Write(text_below_table))
        self.play(FadeOut(VGroup(t1, text_below_table)))
        self.play(Write(cooperation_and_altruism))
        self.play(FadeOut(cooperation_and_altruism))

        hawk_fight = MathTex('{', *division('{{V}}', '2'), '-', *division('{{C}}', '2'), '}')
        hawk_share = MathTex('{{V}}')
        dove_fight = MathTex('0')
        dove_share = MathTex(*division('{{V}}', '2'))

        t2 = GTtable(table_strs=[[hawk_fight, hawk_share], [dove_fight, dove_share]],
                    row_headers=['Hawk meets', 'Dove meets'],
                    col_headers=['Hawk', 'Dove'],
                    table_width = TABLE_WIDTH,
                    table_height = TABLE_HEIGHT,
                    n_rows = 2,
                    n_cols = 2).shift(UP)

        value = MathTex('{{V}}').save_state()
        cost = MathTex('{{C}}').save_state()
        hawks = MathTex('{{H}}').save_state()
        doves = MathTex('{{D}}').save_state()
        value_desc = MathTex(r'\text{--- Value or payoff}').save_state()
        cost_desc = MathTex(r'\text{--- Cost}').save_state()
        hawks_desc = MathTex(r'\text{--- The proportion of hawks}').save_state()
        doves_desc = MathTex(r'\text{--- The proportion of doves}').save_state()
        one_minus_hawks = MathTex('1 - H').save_state()
        
        value_desc.next_to(t2.frame, DOWN)
        value.next_to(value_desc, LEFT)
        cost.next_to(value, DOWN)
        cost_desc.next_to(cost, RIGHT)
        
        self.play(FadeIn(t2.frame))
        
        self.play(Write(t2.get_row_headers()[0]))
        self.play(Write(t2.get_row_headers()[1]))
        self.play(Write(t2.get_col_headers()[0]))
        self.play(Write(t2.get_col_headers()[1]))

        self.play(Write(VGroup(value, value_desc)))
        self.play(Write(VGroup(cost, cost_desc)))

        self.play(TransformMatchingTex(VGroup(value.copy(), cost.copy()), t2.get_payoffs()[0][0][0]))
        self.play(TransformMatchingTex(value.copy(), t2.get_payoffs()[0][1][0]))
        self.play(Create(t2.get_payoffs()[1][0][0]))
        self.play(TransformMatchingTex(value.copy(), t2.get_payoffs()[1][1][0]))
        

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