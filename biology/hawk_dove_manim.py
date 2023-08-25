from manim import *
from manim.opengl import *
import cv2
import numpy as np
from typing import Optional
from scipy.integrate import odeint

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
FONT_SIZE_PREDATOR_PREY = 26
FONT_SIZE_GENERAL = 36
MAIN_COLOR = BLUE_D



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
                 header_col: Optional[str] = WHITE,
                 payoff_col: Optional[str] = WHITE,
                 border_col: Optional[str] = WHITE,
                 **kwargs):
        super().__init__(**kwargs)

        self.table_strs = table_strs
        self.row_headers = row_headers
        self.col_headers = col_headers
        self.table_width = table_width
        self.table_height = table_height
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.text_col = payoff_col
        self.border_col = border_col
        self.header_col = header_col

        self.rows = [VGroup(*[Rectangle(width=table_width/(n_rows+1), height=table_height/(n_cols+1), color=self.border_col) for _ in range(n_cols)]).arrange(buff = 0.0)]

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
                            payoff = Text(payoff, color=self.text_col)
                        payoffs.append(payoff.move_to(self.left_coos[i][j] + k*payoff_space))
                else:
                    self.n_payoffs = 1
                    payoff_space = (self.rigth_coos[i][j]-self.left_coos[i][j])/(self.n_payoffs+1)
                    if isinstance(input_payoffs, str):
                        payoff = Text(payoff, color=self.text_col)
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
        self.row_headers_texts = [Text(header, color=self.header_col).move_to(self.header_coos[0][i]) for i, header in enumerate(self.row_headers)]
        self.col_headers_texts = [Text(header, color=self.header_col).move_to(self.header_coos[1][i]) for i, header in enumerate(self.col_headers)]


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
        return [self.all_payoffs[row][col][i].get_center() for i in range(self.n_payoffs)]


    def get_payoffs(self, row: Optional[int]=None, col: Optional[int]=None, pos: Optional[int]=None):
        if row is None and col is None and pos is None:
            return self.all_payoffs
        
        if row is not None and col is not None and pos is not None:
            return self.all_payoffs[row][col][pos]
        
        row_range = range(len(self.all_payoffs)) if row is None else [row]
        col_range = range(len(self.all_payoffs[0])) if col is None else [col]
        pos_range = range(len(self.all_payoffs[0][0])) if pos is None else [pos]

        if row is not None and col is None and pos is None:
            return [self.all_payoffs[r] for r in row_range]
        
        if row is None and col is not None and pos is None:
            return [[self.all_payoffs[r][c] for r in row_range] for c in col_range]
        
        if row is None and col is None and pos is not None:
            return [[[self.all_payoffs[r][c][p] for c in col_range] for r in row_range] for p in pos_range]
        
        return [[[self.all_payoffs[r][c][p] for p in pos_range] for c in col_range] for r in row_range]


    def get_payoffs_as_list(self):
        return self.list_all_payoffs


    def get_row_headers(self, row: Optional[int] = None):
        if row is None:
            return self.row_headers_texts
        else:
            return self.row_headers_texts[row]


    def get_col_headers(self, col: Optional[int] = None):
        if col is None:
            return(self.col_headers_texts)
        else:
            return(self.col_headers_texts[col])


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

        table_1 = GTtable(table_strs=[[('1', '1'), ('3', '0')], [('0', '3'), ('2', '2')]],
                          row_headers=['Fight', 'Share'],
                          col_headers=['Fight', 'Share'],
                          table_width = TABLE_WIDTH,
                          table_height = TABLE_HEIGHT,
                          n_rows = 2,
                          n_cols = 2,
                          payoff_col = WHITE,
                          header_col = WHITE,
                          border_col = BLUE_D).shift(UP)

        payoffs = table_1.get_payoffs()
        row_headers = table_1.get_row_headers()
        col_headers = table_1.get_col_headers()
        recall_prisoners_dilemma = Text('Let\'s recall prisoner\'s dilemma.')
        cooperation_and_altruism = Text('Cooperation and altruism').to_edge(UL)

        text_below_table = Text('Once again, Prisoner\'s dilemma is \"a reason why we can\'t have nice things.\"', font_size=28, color=WHITE).next_to(table_1.frame.get_bottom(), DOWN).shift(DOWN)

        self.play(Write(recall_prisoners_dilemma))
        self.play(FadeOut(recall_prisoners_dilemma))
        self.play(FadeIn(table_1.frame))

        self.play(AnimationGroup(Write(row_headers[0]), Write(row_headers[1])))
        self.play(AnimationGroup(Write(col_headers[0]), Write(col_headers[1])))
        
        self.play(FadeIn(VGroup(*payoffs[0][0])))
        self.play(FadeIn(VGroup(*payoffs[0][1])))
        self.play(FadeIn(VGroup(*payoffs[1][0])))
        self.play(FadeIn(VGroup(*payoffs[1][1])))

        nash_rects = [SurroundingRectangle(payoffs[0][0][0], color=TEAL_E), SurroundingRectangle(payoffs[0][1][0], color=TEAL_E), SurroundingRectangle(payoffs[0][0][1], color=GOLD_E),
                      SurroundingRectangle(payoffs[1][0][1], color=GOLD_E), SurroundingRectangle(VGroup(payoffs[0][0][0], payoffs[0][0][1]), color=MAROON_E, buff=0.2)]

        for rect in nash_rects:
            self.play(Write(rect))

        self.play(Write(text_below_table))
        self.play(FadeOut(VGroup(table_1, text_below_table)))
        self.play(Write(cooperation_and_altruism))
        self.play(FadeOut(cooperation_and_altruism))

        hawk_fight = MathTex('{', *division('{{V}}', '2'), '-', *division('{{C}}', '2'), '}')
        hawk_share = MathTex('{{V}}')
        dove_fight = MathTex('0')
        dove_share = MathTex(*division('{{V}}', '2'))

        table_2 = GTtable(table_strs=[[hawk_fight, hawk_share], [dove_fight, dove_share]],
                    row_headers=['Hawk meets', 'Dove meets'],
                    col_headers=['Hawk', 'Dove'],
                    table_width = TABLE_WIDTH,
                    table_height = TABLE_HEIGHT,
                    n_rows = 2,
                    n_cols = 2).shift(UP)

        value = MathTex('{{V}}')
        cost = MathTex('{{C}}')
        hawks = MathTex('{{H}}')
        doves = MathTex('{{D}}')
        value_desc = MathTex(r'\text{--- Value or payoff}', font_size=FONT_SIZE_GENERAL)
        cost_desc = MathTex(r'\text{--- Cost}', font_size=FONT_SIZE_GENERAL)
        hawks_desc = MathTex(r'\text{--- The proportion of hawks}', font_size=FONT_SIZE_GENERAL)
        doves_desc = MathTex(r'\text{--- The proportion of doves}', font_size=FONT_SIZE_GENERAL)
        one_minus_hawks = MathTex('1 - H', font_size=FONT_SIZE_GENERAL)

        rabbits = MathTex(r'\text{Rabbits:}', font_size=FONT_SIZE_GENERAL).move_to([-5,1,0])
        rabbits_eq = MathTex(*division('dx', 'dt'), '=', r'\alpha x', '-', r'\beta xy').next_to(rabbits, RIGHT)
        foxes = MathTex('Foxes:', font_size=FONT_SIZE_GENERAL).next_to(rabbits, DOWN)
        foxes_eq = MathTex(*division('dy', 'dt'), '=', r'\gamma xy', '-', r'\delta y').next_to(foxes, RIGHT)

        pp_conds = [['x', 'y', 't', division('dx', 'dt'), division('dy', 'dt'), r'\alpha', r'\beta', r'\gamma', r'\delta'],
                    [r'\text{--- number of rabbits per square km}', r'\text{--- number of foxes per square km}', r'\text{--- time}', r'\text{--- growth rate of rabbits}', r'\text{--- growth rate of rabbits}',
                     r'\text{--- maximum growth rate of rabbits}', r'\text{--- effect of foxes on the growth rate of rabbits}', r'\text{--- effect of rabbits on the growth rate of foxes}', r'\text{--- death rate of foxes}']]
        
        pp_conds_mtex = []
        pp_conds_mtex.append((MathTex(pp_conds[0][0], font_size=FONT_SIZE_PREDATOR_PREY).move_to([0, 3, 0]),
                              MathTex(pp_conds[1][0], font_size=FONT_SIZE_PREDATOR_PREY)))
        pp_conds_mtex[0][1].next_to(pp_conds_mtex[0][0].get_center(), RIGHT)

        for i, _ in enumerate(pp_conds[0][1:], 1):
            if isinstance(pp_conds[0][i], list):
                pp_conds_mtex.append((MathTex(*pp_conds[0][i], font_size=FONT_SIZE_PREDATOR_PREY).align_to(pp_conds_mtex[i-1][0], LEFT).next_to(pp_conds_mtex[i-1][0], DOWN),
                                      MathTex(pp_conds[1][i], font_size=FONT_SIZE_PREDATOR_PREY)))
                pp_conds_mtex[i][1].next_to(pp_conds_mtex[i][0].get_center(), RIGHT)
            else:
                pp_conds_mtex.append((MathTex(pp_conds[0][i], font_size=FONT_SIZE_PREDATOR_PREY).align_to(pp_conds_mtex[i-1][0], LEFT).next_to(pp_conds_mtex[i-1][0], DOWN),
                                      MathTex(pp_conds[1][i], font_size=FONT_SIZE_PREDATOR_PREY)))
                pp_conds_mtex[i][1].next_to(pp_conds_mtex[i][0].get_center(), RIGHT)


        value.next_to(table_2.frame, DOWN).align_to(table_2.frame, LEFT)
        value_desc.next_to(value, RIGHT)
        cost.next_to(value, DOWN)
        cost_desc.next_to(cost, RIGHT)
        hawks.next_to(value_desc, buff=1)
        hawks_desc.next_to(hawks, RIGHT)
        doves.next_to(hawks, DOWN)
        doves_desc.next_to(doves)
        
        self.play(FadeIn(table_2.frame))

        self.play(Write(table_2.get_row_headers(0)))
        self.play(Write(table_2.get_row_headers(1)))
        self.play(Write(table_2.get_col_headers(0)))
        self.play(Write(table_2.get_col_headers(1)))

        self.play(Write(VGroup(value, value_desc)))
        self.play(Write(VGroup(cost, cost_desc)))
        self.play(Write(VGroup(hawks, hawks_desc)))
        self.play(Write(VGroup(doves, doves_desc)))

        self.play(TransformMatchingTex(VGroup(value.copy(), cost.copy()), table_2.get_payoffs(0,0,0)))
        self.play(TransformMatchingTex(value.copy(), table_2.get_payoffs(0,1,0)))
        self.play(Create(table_2.get_payoffs(1,0,0)))
        self.play(TransformMatchingTex(value.copy(), table_2.get_payoffs(1,1,0)))

        ext_table = VGroup(table_2, value_desc, value, cost, cost_desc, hawks, hawks_desc, doves, doves_desc)

        self.play(ext_table.animate.scale(0.5).to_edge(UR))

        calc_eqs = []
        for i, calc in enumerate(calcs):
            # self.wait()
            calc_eqs.append(MathTex(*calc).scale(DEF_SCALE).move_to([-4,3,0]))
            if i == 0:
                self.play(Create(*calc_eqs[i]))
            else:
                calc_eqs[i].next_to(calc_eqs[i-1], DOWN)
                self.play(TransformMatchingTex(calc_eqs[i-1].copy(), calc_eqs[i]))
                 # self.play(TransformMatchingShapes(*calc_eqs[i:i+2]))
        
        self.play(FadeOut(VGroup(*calc_eqs, ext_table)))
        
        for textos, textos2 in pp_conds_mtex:
            self.play(Create(VGroup(textos, textos2)))

        self.play(Create(rabbits))
        self.play(Create(rabbits_eq))
        
        self.play(Create(foxes))
        self.play(Create(foxes_eq))

        self.wait(PAUSE)
