from manim import *
from manim.opengl import *
import cv2
import numpy as np
from typing import Optional
from scipy.integrate import odeint
import numpy as np
from numpy import random
from scipy.integrate import odeint
import pylab as p
from scipy.interpolate import interp1d

custom_tex_template = TexTemplate(documentclass=r"\documentclass[preview, varwidth=2000px]{standalone}")
MathTex.set_default(tex_template=custom_tex_template)

X_MOVE = 5.5
Y_MOVE = 2
PAUSE = 1
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
FONT_SIZE_PREDATOR_PREY = 28
FONT_SIZE_HAWK_DOVE = 36
FONT_SIZE_GENERAL = 42
FONT_SIZE_HEADINGS = 50
MAIN_COLOR = BLUE_D
FONT_BULLETS = 30
FONT_SIZE_AXES = 24


def predator_prey(vars, t, params):
    x = vars[0]
    y = vars[1]
    a = params[0]
    b = params[1]
    c = params[2]
    d = params[3]

    dxdt  =    a*x - b*x*y
    dydt  =  c*x*y - d*y

    return [dxdt, dydt]


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
                 header_font_size: Optional[str] = 36,
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
        self.header_font_size = header_font_size

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
        self.row_headers_texts = [Text(header, color=self.header_col, font_size=self.header_font_size).move_to(self.header_coos[0][i]) for i, header in enumerate(self.row_headers)]
        self.col_headers_texts = [Text(header, color=self.header_col, font_size=self.header_font_size).move_to(self.header_coos[1][i]) for i, header in enumerate(self.col_headers)]


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
            return self.col_headers_texts
        else:
            return self.col_headers_texts[col]


    def get_row_header_coos(self, pos: Optional[int] = None):
        if pos is None:
            return self.header_coos[0]
        else:
            return self.header_coos[0][pos]


    def get_col_header_coos(self, pos: Optional[int] = None):
        if pos is None:
            return self.header_coos[1]
        else:
            return self.header_coos[1][pos]


    def update_header(self, new_header: str, row_col: str, pos: int): # those are likely wrong due to mathtex not using become. Change it to a custom animation, like custom write.
        if row_col.lower() in ('row', 'rows', 'r'):
            self.row_headers_texts[pos].become(Text(new_header).move_to(self.row_headers_texts[pos]))
            self.row_headers_texts[pos] = Text(new_header).move_to(self.row_headers_texts[pos])

        if row_col.lower() in ('col', 'cols', 'c'):
            self.col_headers_texts[pos].become(Text(new_header).move_to(self.col_headers_texts[pos]))
            self.col_headers_texts[pos] = Text(new_header).move_to(self.col_headers_texts[pos])


    def update_payoff(self, new_payoff: str | Mobject, row: int, col: int, pos: int):
        if isinstance(new_payoff, str):
            new_payoff = Text(new_payoff)
        self.all_payoffs[row][col][pos].become(new_payoff.move_to(self.all_payoffs[row][col][pos]))
        self.all_payoffs[row][col][pos] = new_payoff.move_to(self.all_payoffs[row][col][pos])


class Biology(Scene):
    def construct(self):
        conds = ([r'V > C'],
                 [r'V < C'],
                 [r'H > \frac{V}{C}'],
                 [r'H < \frac{V}{C}'])

## Prisoner's dilemma
        table_1 = GTtable(table_strs=[[('1', '1'), ('3', '0')], [('0', '3'), ('2', '2')]],
                          row_headers=['Fight', 'Share'],
                          col_headers=['Fight', 'Share'],
                          table_width = TABLE_WIDTH,
                          table_height = TABLE_HEIGHT,
                          n_rows = 2,
                          n_cols = 2,
                          payoff_col = WHITE,
                          header_col = WHITE,
                          border_col = BLUE_D,
                          header_font_size = 30).shift(UP)

        payoffs = table_1.get_payoffs()
        row_headers = table_1.get_row_headers()
        col_headers = table_1.get_col_headers()
        recall_prisoners_dilemma = Text('Let\'s recall prisoner\'s dilemma.')

        text_below_table = Text('Once again, Prisoner\'s dilemma is \"a reason why we can\'t have nice things.\"', font_size=28, color=WHITE).next_to(table_1.frame.get_bottom(), DOWN).shift(DOWN)
        texts_target_for_future = text_below_table.get_center()

        self.play(Write(recall_prisoners_dilemma))
        self.play(FadeOut(recall_prisoners_dilemma))
        self.play(FadeIn(table_1.frame))

        self.play(AnimationGroup(Write(row_headers[0]), Write(row_headers[1])))
        self.play(AnimationGroup(Write(col_headers[0]), Write(col_headers[1])))
        
        self.play(Write(VGroup(*payoffs[0][0])))
        self.play(Write(VGroup(*payoffs[0][1])))
        self.play(Write(VGroup(*payoffs[1][0])))
        self.play(Write(VGroup(*payoffs[1][1])))

        nash_rects = [SurroundingRectangle(payoffs[0][0][0], color=TEAL_E), SurroundingRectangle(payoffs[0][1][0], color=TEAL_E), SurroundingRectangle(payoffs[0][0][1], color=GOLD_E),
                      SurroundingRectangle(payoffs[1][0][1], color=GOLD_E), SurroundingRectangle(VGroup(payoffs[0][0][0], payoffs[0][0][1]), color=MAROON_E, buff=0.2)]

        for rect in nash_rects:
            self.play(Write(rect))

        self.play(Write(text_below_table))
        self.play(FadeOut(VGroup(*nash_rects, table_1, text_below_table)))

## Theory about cooperation
        line_1 = Line(start=[-0.5,1,0], end=[-5.5,1,0], stroke_width=0.8)
        line_2 = Line(start=[0.5,1,0], end=[5.5,1,0], stroke_width=0.8)
        line_3 = Line(start=[0,0.9,0], end=[0,-3.5,0], stroke_width=0.8)
        cooperation_and_altruism = Tex('Cooperation and altruism', font_size=FONT_SIZE_HEADINGS).to_edge(UL)
        why_coop = Tex('Why would animals cooperate? How could altruism survive?', font_size=40).move_to([0,1.8,0])
        
        group_sel = Tex(r'\textbf{Group selection}', font_size=36).next_to(line_1, 2*DOWN)#.align_to(line_1, RIGHT).shift(LEFT)
        self_gene = Tex(r'\textbf{Selfish gene}', font_size=36).next_to(line_2, 2*DOWN)#.align_to(line_2, LEFT).shift(RIGHT)
        
        gs_b1 = Tex('Individuals do it for the good of the group', font_size=FONT_BULLETS).next_to(group_sel, 3*DOWN)
        gs_b2 = Tex('Minority view', font_size=FONT_BULLETS).next_to(gs_b1, 3*DOWN).set_color(MAROON_D)

        sg_b1 = Tex('Sharing strategy may be self-serving', font_size=FONT_BULLETS).next_to(self_gene, 3*DOWN)
        sg_b2 = Tex('Majority view', font_size=FONT_BULLETS).next_to(sg_b1, 3*DOWN).set_color(GREEN_C)


        self.play(Write(cooperation_and_altruism))
        self.play(Write(why_coop[:25]))
        self.play(Write(why_coop[25:]))
        self.play(*[Write(line) for line in [line_1, line_2, line_3]])
        self.play(Write(group_sel))
        self.play(Write(gs_b1))
        self.play(Write(self_gene))
        self.play(Write(sg_b1))
        self.play(Write(gs_b2), Write(sg_b2))
        self.play(*[FadeOut(mobj) for mobj in [line_1, line_2, line_3, cooperation_and_altruism, why_coop, group_sel, self_gene, gs_b1, gs_b2, sg_b1, sg_b2]])

## Hawk and Dove
        eqs = MathTex(r'EV_H &= EV_D\\',
                r'H \big( {V \over 2} - {C \over 2} \big) + DV &= 0 + D {V \over 2}\\',
                r'HV - HC + 2DV &= DV\\',
                r'HV - HC &= -DV\\',
                r'HV - HC &= -(1-H)V\\',
                r'HV - HC &= HV - V\\',
                r'- HC &= -V\\',
                r'HC &= V\\',
                r'H &= {V \over C}\\',
                font_size=FONT_SIZE_HAWK_DOVE).to_edge(UL)
        for eq in eqs: index_labels(eq)

        hawk_fight = MathTex(r'{V \over 2} - {C \over 2}')
        hawk_share = MathTex('V')
        dove_fight = MathTex('0')
        dove_share = MathTex(r'{V \over 2}')

        table_2 = GTtable(table_strs=[[hawk_fight, hawk_share], [dove_fight, dove_share]],
                    row_headers=['Hawk meets', 'Dove meets'],
                    col_headers=['Hawk', 'Dove'],
                    table_width = TABLE_WIDTH,
                    table_height = TABLE_HEIGHT,
                    n_rows = 2,
                    n_cols = 2,
                    payoff_col = WHITE,
                    header_col = WHITE,
                    border_col = BLUE_D,
                    header_font_size = 30).shift(UP)

        value = MathTex('V')
        cost = MathTex('C')
        hawks = MathTex('H')
        doves = MathTex('D')
        value_desc = MathTex(r'\text{--- Value or payoff}', font_size=FONT_SIZE_GENERAL)
        cost_desc = MathTex(r'\text{--- Cost}', font_size=FONT_SIZE_GENERAL)
        hawks_desc = MathTex(r'\text{--- Proportion of hawks}', font_size=FONT_SIZE_GENERAL)
        doves_desc = MathTex(r'\text{--- Proportion of doves}', font_size=FONT_SIZE_GENERAL)
        one_minus_hawks = MathTex('1 - H', font_size=FONT_SIZE_GENERAL)

        value.next_to(table_2.frame, DOWN).align_to(table_2.frame, LEFT)
        value_desc.next_to(value, RIGHT)
        cost.next_to(value, DOWN)
        cost_desc.next_to(cost, RIGHT)
        hawks.next_to(value_desc, buff=1)
        hawks_desc.next_to(hawks, RIGHT)
        doves.next_to(hawks, DOWN)
        doves_desc.next_to(doves)
        ext_table = VGroup(table_2, value_desc, value, cost, cost_desc, hawks, hawks_desc, doves, doves_desc)

        index_labels(table_2.get_payoffs(0,0,0)[0])

        self.play(FadeIn(table_2.frame))

        self.play(Write(table_2.get_row_headers(0)))
        self.play(Write(table_2.get_row_headers(1)))
        self.play(Write(table_2.get_col_headers(0)))
        self.play(Write(table_2.get_col_headers(1)))

        self.play(Write(VGroup(value, value_desc)))
        self.play(Write(VGroup(cost, cost_desc)))
        self.play(Write(VGroup(hawks, hawks_desc)))
        self.play(Write(VGroup(doves, doves_desc)))

        val_copy = value.copy()
        cost_copy = cost.copy()
        val_copy2 = value.copy()
        cost_copy2 = cost.copy()
        val_copy3 = value.copy()
        
        self.play(AnimationGroup(val_copy.animate.move_to(table_2.get_payoffs(0,0,0)[0][0]), FadeIn(table_2.get_payoffs(0,0,0)[0][1:3])))
        self.play(cost_copy.animate.move_to(table_2.get_payoffs(0,0,0)[0][4]), FadeIn(table_2.get_payoffs(0,0,0)[0][3]), FadeIn(table_2.get_payoffs(0,0,0)[0][5:]))
        self.play(val_copy2.animate.move_to(table_2.get_payoffs(0,1,0)[0][0]))
        self.play(Create(table_2.get_payoffs(1,0,0)))
        self.play(val_copy3.animate.move_to(table_2.get_payoffs(1,1,0)[0][0]), FadeIn(table_2.get_payoffs(1,1,0)[0][1:]))
        self.add(table_2.get_payoffs(0,0,0), table_2.get_payoffs(0,1,0), table_2.get_payoffs(1,1,0))
        self.remove(val_copy, cost_copy, val_copy2, cost_copy2, val_copy3)

        self.play(ext_table.animate.scale(0.5).to_edge(UR))

# 1st eq
        self.play(Write(eqs[0]))
# 2nd eq
        copy_0_0 = table_2.get_payoffs(0,0,0).copy()
        copy_0_1 = table_2.get_payoffs(0,1,0).copy()
        copy_1_0 = table_2.get_payoffs(1,0,0).copy()
        copy_1_1 = table_2.get_payoffs(1,1,0).copy()
        h_copy = hawks.copy()
        d_copy = doves.copy()
        d_copy2 = doves.copy()
        self.play(FadeIn(eqs[1][13]))
        self.play(Indicate(hawks))
        self.play(h_copy.animate.move_to(eqs[1][0]).match_width(eqs[1][0]))
        self.play(Indicate(table_2.get_payoffs(0,0,0)))
        self.play(FadeIn(eqs[1][1]), FadeIn(eqs[1][9]), copy_0_0.animate.move_to(eqs[1][2:9]).match_width(eqs[1][2:9]))
        self.play(FadeIn(eqs[1][10]))
        self.play(Indicate(doves))
        self.play(d_copy.animate.move_to(eqs[1][11]).match_width(eqs[1][11]))
        self.play(Indicate(table_2.get_payoffs(0,1,0)))
        self.play(copy_0_1.animate.move_to(eqs[1][12]).match_width(eqs[1][12]))
        self.play(Indicate(table_2.get_payoffs(1,0,0)))
        self.play(copy_1_0.animate.move_to(eqs[1][14]).match_width(eqs[1][14]))
        self.play(FadeIn(eqs[1][15]))
        self.play(Indicate(doves))
        self.play(d_copy2.animate.move_to(eqs[1][16]).match_width(eqs[1][16]))
        self.play(Indicate(table_2.get_payoffs(1,1,0)))
        self.play(copy_1_1.animate.move_to(eqs[1][17:20]).match_width(eqs[1][17:20]))
# 3rd eq
        eqs1_copy = eqs[1].copy()
        eqs1_copy2 = eqs[1].copy()
        self.play(FadeIn(eqs[2][9]))
        self.play(eqs1_copy[0].animate.move_to(eqs[2][0]),
                  eqs1_copy[2].animate.move_to(eqs[2][1]),
                  eqs1_copy[5].animate.move_to(eqs[2][2]),
                  eqs1_copy2[0].animate.move_to(eqs[2][3]),
                  eqs1_copy[6].animate.move_to(eqs[2][4]))
        self.play(eqs1_copy[10].animate.move_to(eqs[2][5]),
                  FadeIn(eqs[2][6]),
                  eqs1_copy[11].animate.move_to(eqs[2][7]),
                  eqs1_copy[12].animate.move_to(eqs[2][8]))
        self.play(eqs1_copy[16].animate.move_to(eqs[2][10]),
                  eqs1_copy[17].animate.move_to(eqs[2][11]))
# 4th eq
        self.play(FadeIn(eqs[3][5]))
        self.play(eqs[2][0:5].animate.move_to(eqs[3][0:5]))
        self.play(FadeIn(eqs[3][6]), eqs[2][10:12].animate.move_to(eqs[3][7:9]))
# 5th eq
        copy_3_6 = eqs[3][6].copy()
        copy_3_7 = eqs[3][7].copy()
        self.play(FadeIn(eqs[4][5]))
        self.play(eqs[3][0:5].animate.move_to(eqs[4][0:5]))
        self.play(copy_3_6.animate.move_to(eqs[4][6]),
                  FadeIn(eqs[4][7]), FadeIn(eqs[4][11]), Transform(copy_3_7, eqs[4][8:11]),
                  eqs[3][8].animate.move_to(eqs[4][12]))
# 6th eq
        self.play(FadeIn(eqs[5][5]))
        self.play(eqs[4][0:5].animate.move_to(eqs[5][0:5]))
        self.play(eqs[4][6].animate.move_to(eqs[5][8]),
                  eqs[4][9].animate.move_to(eqs[5][8]),
                  eqs[4][10].animate.move_to(eqs[5][6]),
                  Transform(VGroup(eqs[4][8], eqs[4][12]), eqs[5][7]),
                  eqs[4][12].animate.move_to(eqs[5][9]))
# 7th eq
        self.play(FadeIn(eqs[6][3]))
        self.play(eqs[5][2:5].animate.move_to(eqs[6][0:3]))
        self.play(eqs[5][8:10].animate.move_to(eqs[6][4:6]))
# 8th eq
        self.play(FadeIn(eqs[7][2]))
        self.play(eqs[6][1:3].animate.move_to(eqs[7][0:2]))
        self.play(eqs[6][5].animate.move_to(eqs[7][3]))
# 9th eq
        copy_7_2 = eqs[7][2].copy()
        self.play(eqs[7][0].animate.move_to(eqs[8][0]),
                  copy_7_2.animate.move_to(eqs[8][1]),
                  eqs[7][3].animate.move_to(eqs[8][2]),
                  FadeIn(eqs[8][3]),
                  eqs[7][1].animate.move_to(eqs[8][4]))
        
        self.add(eqs[8])
        
        conds = MathTex(r'V &> C \implies H = 1,\quad{} D = 0 \\',
                        r'V &< C \implies H < 1,\quad{} D > 0 \\', font_size=FONT_SIZE_HAWK_DOVE)
        conds2 = MathTex(r'H &> \frac{V}{C},\quad{} \text{playing Dove yields higher EV} \\',
                         r'H &< \frac{V}{C},\quad{} \text{playing Hawk yields higher EV} \\', font_size=FONT_SIZE_HAWK_DOVE)
        conclusion_h_d = Tex('Playing Dove can be a viable strategy. Individuals might be sharers for their own benefit.')
        
        index_labels(conds)
        conds.next_to(eqs[8][3], 3*RIGHT)
        conds[0].shift(0.2*UP)
        conds[1].shift(0.2*DOWN)
        brace = BraceBetweenPoints(conds.get_top(), conds.get_bottom()).next_to(conds, 0.8*LEFT)
        resulting_conditions = VGroup(eqs[8], brace, conds)
        self.play(GrowFromCenter(brace))
        self.play(Write(conds[0]))
        self.play(Write(conds[1]))
        self.play(FadeOut(eqs[0:8]), *[FadeOut(mob) for mob in [copy_0_0, copy_1_0, copy_0_1, copy_1_1, eqs1_copy, h_copy, d_copy, copy_3_6, copy_7_2, d_copy2, copy_3_7, eqs1_copy2]])
        self.play(resulting_conditions.animate.to_edge(UL).shift(DOWN))

        v_leq_c = conds[1][0:3].copy()

        brace2 = BraceBetweenPoints(conds2.get_top(), conds2.get_bottom()).next_to(brace, 6*DOWN)
        conds2[0].next_to(brace2, RIGHT).align_to(brace2, UP)
        conds2[1].next_to(brace2, RIGHT).next_to(conds2[0], DOWN)
        brace_copy = brace.copy()
        conclusion_h_d.move_to(texts_target_for_future)
        self.play(Transform(brace_copy, brace2), v_leq_c.animate.next_to(brace2, LEFT))
        self.play(Write(conds2[0]))
        self.play(Write(conds2[1]))
        self.play(Write(conclusion_h_d))
        self.play(*[FadeOut(mob) for mob in [ext_table, resulting_conditions, v_leq_c, brace2, brace_copy, conds2, conclusion_h_d]])
## Predator-Prey introduction
        fox_path = r"C:\Users\Honzík\OneDrive - Vysoká škola ekonomická v Praze\Connection\Plocha\Ucení\Game theory\biology\fox.png"
        rab_path = r"C:\Users\Honzík\OneDrive - Vysoká škola ekonomická v Praze\Connection\Plocha\Ucení\Game theory\biology\rabbit.png"
        foxrab_path = r"C:\Users\Honzík\OneDrive - Vysoká škola ekonomická v Praze\Connection\Plocha\Ucení\Game theory\biology\fox_v_rabbit.png"

        # Create an ImageMobject with the image
        fox_img_dot = Dot().move_to([-1,0,0])
        rab_img_dot = Dot().move_to([1,0,0])
        fox_img = ImageMobject(fox_path)
        rab_img = ImageMobject(rab_path)
        foxrab_img = ImageMobject(foxrab_path)

        # Set the position and scale of the image
        fox_img.scale(1.5).align_to(fox_img_dot, RIGHT)
        rab_img.scale(1.5).align_to(rab_img_dot, LEFT)
        crossos = Cross(color=MAROON_D, stroke_width=20, scale_factor=.2)
        foxrab_img.scale(1.8).move_to([0,-1,0])

        self.play(FadeIn(fox_img))
        self.play(Write(crossos))
        self.play(FadeIn(rab_img))
        self.play(fox_img.animate.shift(UP), rab_img.animate.shift(UP), crossos.animate.shift(UP))
        self.play(FadeIn(foxrab_img))
        self.play(*[FadeOut(mob)for mob in [fox_img, rab_img, foxrab_img, crossos]])
## Predator-Prey
        predator_prey_heading = Tex('Predator-pray', font_size=FONT_SIZE_HEADINGS).to_edge(UL)

        pp_conds = [['x', 'y', 't', r'{dx \over dt}', r'{dy \over dt}', r'\alpha', r'\beta', r'\gamma', r'\delta'],
                    [r'\text{--- number of rabbits per square km}', r'\text{--- number of foxes per square km}', r'\text{--- time}', r'\text{--- growth rate of rabbits}', r'\text{--- growth rate of rabbits}',
                     r'\text{--- maximum growth rate of rabbits}', r'\text{--- effect of foxes on the growth rate of rabbits}', r'\text{--- effect of rabbits on the growth rate of foxes}', r'\text{--- death rate of foxes}']]

        pp_conds_mtex = []
        pp_conds_mtex.append((MathTex(pp_conds[0][0], font_size=FONT_SIZE_PREDATOR_PREY).move_to([1, 2, 0]),
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

        t = np.linspace(0, 10, num=10000)
        a = 1.5
        b = 1.5
        c = 1
        d = 2
        vars_0 = [1, 2]
        params = [a, b, c, d]
        y = odeint(predator_prey, vars_0, t, args=(params,))

        xpos = ValueTracker(0)
        n_rabbits = Integer(100).scale(0.75)
        n_foxes = Integer(200).scale(0.75)

        prey_intpol = interp1d(t, y[:,0], kind='cubic')
        predator_intpol = interp1d(t, y[:,1], kind='cubic')

        ax = Axes(x_range=[0, 12, 1], y_range=[0, 5, 1], x_length=6, y_length=2, tips=False, x_axis_config={"include_ticks": False}, y_axis_config={"include_ticks": False})
        ax.shift(4 * RIGHT + 1 * UP)
        ax2 = Axes(x_range=[0, 12, 1], y_range=[0, 5, 1], x_length=6, y_length=2, tips=False, x_axis_config={"include_ticks": False}, y_axis_config={"include_ticks": False}).next_to(ax, DOWN)
        time = Tex('Time', font_size=FONT_SIZE_AXES).next_to(ax2, DOWN)
        rabbit_y = Tex('Number of rabbits', font_size=FONT_SIZE_AXES).rotate(90*DEGREES)
        fox_y = Tex('Number of foxes', font_size=FONT_SIZE_AXES).rotate(90*DEGREES)
        
        rabbit_y.next_to(ax, LEFT)
        fox_y.next_to(ax2, LEFT)
        
        p_p_eq = Tex(r'2 equilibria exists:',
                     r'1) $x=0$ and $y=0$, both extinct',
                     r'2) $x=\frac{\delta}{\gamma}$ and $y=\frac{\alpha}{\beta}$, population of rabbits depends on parameters of foxes and vice versa',
                     r'But eq. 2) is unstable $\implies$ any disturbance leads to oscillation', font_size=FONT_SIZE_PREDATOR_PREY)

        p_p_eq[3].to_edge(DL)
        p_p_eq[2].next_to(p_p_eq[3], 1.5*UP).align_to(p_p_eq[3] ,LEFT).shift(RIGHT)
        p_p_eq[1].next_to(p_p_eq[2], UP).align_to(p_p_eq[2] ,LEFT)
        p_p_eq[0].next_to(p_p_eq[1], 1.5*UP).align_to(p_p_eq[3] ,LEFT)

        rabbits_eq = MathTex(r'{dx \over dt} = \alpha x - \beta xy').next_to(ax, LEFT).shift(LEFT)
        foxes_eq = MathTex(r'{dy \over dt} = -\gamma y - \delta xy').next_to(ax2, LEFT).align_to(rabbits_eq, LEFT)

        rabbits = Tex('Rabbits:', font_size=FONT_SIZE_GENERAL).next_to(rabbits_eq, LEFT).shift(0.5*LEFT)
        foxes = Tex('Foxes:', font_size=FONT_SIZE_GENERAL).next_to(foxes_eq, LEFT).align_to(rabbits, RIGHT)

        prey = always_redraw(lambda: ax.plot(prey_intpol, x_range=[0, xpos.get_value(), 0.01], color=BLUE_D))
        predator = always_redraw(lambda: ax2.plot(predator_intpol, x_range=[0, xpos.get_value(), 0.01], color=MAROON_D))

        line = DashedLine(start=ax.coords_to_point(xpos.get_value(), prey_intpol(xpos.get_value()), -0.1), end=ax2.coords_to_point(xpos.get_value(), predator_intpol(xpos.get_value()), -0.01), color=TEAL_B, dashed_ratio=0.3)
        line.add_updater(lambda m: m.put_start_and_end_on(ax.c2p(xpos.get_value(), prey_intpol(xpos.get_value()), -0.1), ax2.c2p(xpos.get_value(), predator_intpol(xpos.get_value()), -0.01)))

        def rabbit_updater(mobj):
            mobj.next_to(ax.c2p(xpos.get_value(), prey_intpol(xpos.get_value())), UR).set_value(prey_intpol(xpos.get_value())*100)

        def fox_updater(mobj):
            mobj.next_to(ax2.c2p(xpos.get_value(), predator_intpol(xpos.get_value())), UR).set_value(predator_intpol(xpos.get_value())*100)

        n_rabbits.add_updater(rabbit_updater)
        n_foxes.add_updater(fox_updater)

        self.play(Write(predator_prey_heading))

        for line1, line2 in pp_conds_mtex:
            self.play(Create(VGroup(line1, line2)))

        self.play(FadeIn(rabbits))
        self.play(FadeIn(rabbits_eq))
        
        self.play(FadeIn(foxes))
        self.play(FadeIn(foxes_eq))
        self.play(*[FadeOut(VGroup(line1, line2)) for line1, line2 in pp_conds_mtex])

        self.play(FadeIn(ax),FadeIn(ax2))
        self.play(FadeIn(time))
        self.play(FadeIn(rabbit_y), FadeIn(fox_y))
        self.add(prey, predator, line)


        self.play(FadeIn(n_rabbits),FadeIn(n_foxes))
        self.play(xpos.animate.set_value(10), run_time=30, rate_func=rate_functions.linear)
        second_last_scene = VGroup(ax, ax2, n_rabbits, n_foxes, time, rabbit_y, fox_y, rabbits_eq, foxes_eq, rabbits, foxes)
        self.play(second_last_scene.animate.shift(UP).scale(0.7))
        for line in p_p_eq:
            self.play(FadeIn(line))
        self.wait()

        self.wait(PAUSE)


class Main(Scene):
    def construct(self):
        eqs = MathTex(r'EV_H &= EV_D\\',
                r'H \big( {V \over 2} - {C \over 2} \big) + DV &= 0 + D {V \over 2}\\',
                r'HV - HC + 2DV &= DV\\',
                r'HV - HC &= -DV\\',
                r'HV - HC &= -(1-H)V\\',
                r'HV - HC &= HV - V\\',
                r'- HC &= -V\\',
                r'HC &= V\\',
                r'H &= {V \over C}\\',
                font_size=FONT_SIZE_HAWK_DOVE).to_edge(UL)
        for eq in eqs: index_labels(eq)

        hawk_fight = MathTex(r'{V \over 2} - {C \over 2}')
        hawk_share = MathTex('V')
        dove_fight = MathTex('0')
        dove_share = MathTex(r'{V \over 2}')

        table_2 = GTtable(table_strs=[[hawk_fight, hawk_share], [dove_fight, dove_share]],
                    row_headers=['Hawk meets', 'Dove meets'],
                    col_headers=['Hawk', 'Dove'],
                    table_width = TABLE_WIDTH,
                    table_height = TABLE_HEIGHT,
                    n_rows = 2,
                    n_cols = 2,
                    payoff_col = WHITE,
                    header_col = WHITE,
                    border_col = BLUE_D,
                    header_font_size = 30).shift(UP)

        value = MathTex('V')
        cost = MathTex('C')
        hawks = MathTex('H')
        doves = MathTex('D')
        value_desc = MathTex(r'\text{--- Value or payoff}', font_size=FONT_SIZE_GENERAL)
        cost_desc = MathTex(r'\text{--- Cost}', font_size=FONT_SIZE_GENERAL)
        hawks_desc = MathTex(r'\text{--- Proportion of hawks}', font_size=FONT_SIZE_GENERAL)
        doves_desc = MathTex(r'\text{--- Proportion of doves}', font_size=FONT_SIZE_GENERAL)
        one_minus_hawks = MathTex('1 - H', font_size=FONT_SIZE_GENERAL)

        value.next_to(table_2.frame, DOWN).align_to(table_2.frame, LEFT)
        value_desc.next_to(value, RIGHT)
        cost.next_to(value, DOWN)
        cost_desc.next_to(cost, RIGHT)
        hawks.next_to(value_desc, buff=1)
        hawks_desc.next_to(hawks, RIGHT)
        doves.next_to(hawks, DOWN)
        doves_desc.next_to(doves)
        ext_table = VGroup(table_2, value_desc, value, cost, cost_desc, hawks, hawks_desc, doves, doves_desc)

        index_labels(table_2.get_payoffs(0,0,0)[0])

        self.play(FadeIn(table_2.frame))

        self.play(Write(table_2.get_row_headers(0)))
        self.play(Write(table_2.get_row_headers(1)))
        self.play(Write(table_2.get_col_headers(0)))
        self.play(Write(table_2.get_col_headers(1)))

        self.play(Write(VGroup(value, value_desc)))
        self.play(Write(VGroup(cost, cost_desc)))
        self.play(Write(VGroup(hawks, hawks_desc)))
        self.play(Write(VGroup(doves, doves_desc)))

        val_copy = value.copy()
        cost_copy = cost.copy()
        val_copy2 = value.copy()
        cost_copy2 = cost.copy()
        val_copy3 = value.copy()
        
        self.play(AnimationGroup(val_copy.animate.move_to(table_2.get_payoffs(0,0,0)[0][0]), FadeIn(table_2.get_payoffs(0,0,0)[0][1:3])))
        self.play(cost_copy.animate.move_to(table_2.get_payoffs(0,0,0)[0][4]), FadeIn(table_2.get_payoffs(0,0,0)[0][3]), FadeIn(table_2.get_payoffs(0,0,0)[0][5:]))
        self.play(val_copy2.animate.move_to(table_2.get_payoffs(0,1,0)[0][0]))
        self.play(Create(table_2.get_payoffs(1,0,0)))
        self.play(val_copy3.animate.move_to(table_2.get_payoffs(1,1,0)[0][0]), FadeIn(table_2.get_payoffs(1,1,0)[0][1:]))
        self.add(table_2.get_payoffs(0,0,0), table_2.get_payoffs(0,1,0), table_2.get_payoffs(1,1,0))
        self.remove(val_copy, cost_copy, val_copy2, cost_copy2, val_copy3)

        self.play(ext_table.animate.scale(0.5).to_edge(UR))

# 1st eq
        self.play(Write(eqs[0]))
# 2nd eq
        copy_0_0 = table_2.get_payoffs(0,0,0).copy()
        copy_0_1 = table_2.get_payoffs(0,1,0).copy()
        copy_1_0 = table_2.get_payoffs(1,0,0).copy()
        copy_1_1 = table_2.get_payoffs(1,1,0).copy()
        h_copy = hawks.copy()
        d_copy = doves.copy()
        d_copy2 = doves.copy()
        self.play(FadeIn(eqs[1][13]))
        self.play(Indicate(hawks))
        self.play(h_copy.animate.move_to(eqs[1][0]).match_width(eqs[1][0]))
        self.play(Indicate(table_2.get_payoffs(0,0,0)))
        self.play(FadeIn(eqs[1][1]), FadeIn(eqs[1][9]), copy_0_0.animate.move_to(eqs[1][2:9]).match_width(eqs[1][2:9]))
        self.play(FadeIn(eqs[1][10]))
        self.play(Indicate(doves))
        self.play(d_copy.animate.move_to(eqs[1][11]).match_width(eqs[1][11]))
        self.play(Indicate(table_2.get_payoffs(0,1,0)))
        self.play(copy_0_1.animate.move_to(eqs[1][12]).match_width(eqs[1][12]))
        self.play(Indicate(table_2.get_payoffs(1,0,0)))
        self.play(copy_1_0.animate.move_to(eqs[1][14]).match_width(eqs[1][14]))
        self.play(FadeIn(eqs[1][15]))
        self.play(Indicate(doves))
        self.play(d_copy2.animate.move_to(eqs[1][16]).match_width(eqs[1][16]))
        self.play(Indicate(table_2.get_payoffs(1,1,0)))
        self.play(copy_1_1.animate.move_to(eqs[1][17:20]).match_width(eqs[1][17:20]))
# 3rd eq
        eqs1_copy = eqs[1].copy()
        eqs1_copy2 = eqs[1].copy()
        self.play(FadeIn(eqs[2][9]))
        self.play(eqs1_copy[0].animate.move_to(eqs[2][0]),
                  eqs1_copy[2].animate.move_to(eqs[2][1]),
                  eqs1_copy[5].animate.move_to(eqs[2][2]),
                  eqs1_copy2[0].animate.move_to(eqs[2][3]),
                  eqs1_copy[6].animate.move_to(eqs[2][4]))
        self.play(eqs1_copy[10].animate.move_to(eqs[2][5]),
                  FadeIn(eqs[2][6]),
                  eqs1_copy[11].animate.move_to(eqs[2][7]),
                  eqs1_copy[12].animate.move_to(eqs[2][8]))
        self.play(eqs1_copy[16].animate.move_to(eqs[2][10]),
                  eqs1_copy[17].animate.move_to(eqs[2][11]))
# 4th eq
        self.play(FadeIn(eqs[3][5]))
        self.play(eqs[2][0:5].animate.move_to(eqs[3][0:5]))
        self.play(FadeIn(eqs[3][6]), eqs[2][10:12].animate.move_to(eqs[3][7:9]))
# 5th eq
        copy_3_6 = eqs[3][6].copy()
        copy_3_7 = eqs[3][7].copy()
        self.play(FadeIn(eqs[4][5]))
        self.play(eqs[3][0:5].animate.move_to(eqs[4][0:5]))
        self.play(copy_3_6.animate.move_to(eqs[4][6]),
                  FadeIn(eqs[4][7]), FadeIn(eqs[4][11]), Transform(copy_3_7, eqs[4][8:11]),
                  eqs[3][8].animate.move_to(eqs[4][12]))
# 6th eq
        self.play(FadeIn(eqs[5][5]))
        self.play(eqs[4][0:5].animate.move_to(eqs[5][0:5]))
        self.play(eqs[4][6].animate.move_to(eqs[5][8]),
                  eqs[4][9].animate.move_to(eqs[5][8]),
                  eqs[4][10].animate.move_to(eqs[5][6]),
                  Transform(VGroup(eqs[4][8], eqs[4][12]), eqs[5][7]),
                  eqs[4][12].animate.move_to(eqs[5][9]))
# 7th eq
        self.play(FadeIn(eqs[6][3]))
        self.play(eqs[5][2:5].animate.move_to(eqs[6][0:3]))
        self.play(eqs[5][8:10].animate.move_to(eqs[6][4:6]))
# 8th eq
        self.play(FadeIn(eqs[7][2]))
        self.play(eqs[6][1:3].animate.move_to(eqs[7][0:2]))
        self.play(eqs[6][5].animate.move_to(eqs[7][3]))
# 9th eq
        copy_7_2 = eqs[7][2].copy()
        self.play(eqs[7][0].animate.move_to(eqs[8][0]),
                  copy_7_2.animate.move_to(eqs[8][1]),
                  eqs[7][3].animate.move_to(eqs[8][2]),
                  FadeIn(eqs[8][3]),
                  eqs[7][1].animate.move_to(eqs[8][4]))
        
        self.add(eqs[8])
        
        conds = MathTex(r'V &> C \implies H = 1,\quad{} D = 0 \\',
                        r'V &< C \implies H < 1,\quad{} D > 0 \\', font_size=FONT_SIZE_HAWK_DOVE)
        conds2 = MathTex(r'H &> \frac{V}{C},\quad{} \text{playing Dove yields higher EV} \\',
                         r'H &< \frac{V}{C},\quad{} \text{playing Hawk yields higher EV} \\', font_size=FONT_SIZE_HAWK_DOVE)
        conclusion_h_d = Tex('Playing Dove can be a viable strategy. Individuals might be sharers for their own benefit.')
        
        index_labels(conds)
        conds.next_to(eqs[8][3], 3*RIGHT)
        conds[0].shift(0.2*UP)
        conds[1].shift(0.2*DOWN)
        brace = BraceBetweenPoints(conds.get_top(), conds.get_bottom()).next_to(conds, 0.8*LEFT)
        resulting_conditions = VGroup(eqs[8], brace, conds)
        self.play(GrowFromCenter(brace))
        self.play(Write(conds[0]), Write(conds[1]))
        self.play(FadeOut(eqs[0:8]), *[FadeOut(mob) for mob in [copy_0_0, copy_1_0, copy_0_1, copy_1_1, eqs1_copy, h_copy, d_copy, copy_3_6, copy_7_2, d_copy2, copy_3_7, eqs1_copy2]])
        self.play(resulting_conditions.animate.to_edge(UL).shift(DOWN))

        v_leq_c = conds[1][0:3].copy()


        brace2 = BraceBetweenPoints(conds2.get_top(), conds2.get_bottom()).next_to(brace, 6*DOWN)
        conds2[0].next_to(brace2, RIGHT).align_to(brace2, UP)
        conds2[1].next_to(brace2, RIGHT).next_to(conds2[0], DOWN)
        brace_copy = brace.copy()
        conclusion_h_d.move_to(texts_target_for_future)
        self.play(Transform(brace_copy, brace2), v_leq_c.animate.next_to(brace2, LEFT))
        self.play(Write(conds2[0]))
        self.play(Write(conds2[1]))

        
        self.wait()