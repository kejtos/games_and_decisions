from manim import *
from manim.opengl import *
import numpy as np

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
                 row_headers: list[str],
                 col_headers: list[str],
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

        row_headers_cells = self.rows[0].copy().next_to(self.rows[0], UP, buff=0.0)
        col_headers_cells = VGroup(*[row[0] for row in self.rows]).copy().next_to(self.rows[0][0], LEFT, buff=0.0).align_to(self.rows[0][0], UP)

        self.table_frame = VGroup(*self.rows, row_headers_cells, col_headers_cells).move_to(ORIGIN)

        self._set_header_coos(row_headers_cells, col_headers_cells)


        row_headers_texts = [Text(text).move_to(header_coos[0][i]) for i, text in enumerate(row_headers)]
        col_headers_texts = [Text(text).move_to(header_coos[1][i]) for i, text in enumerate(col_headers)]

        coos = np.empty((n_rows, n_cols), dtype=object)
        left_coos = np.empty((n_rows, n_cols), dtype=object)
        rigth_coos = np.empty((n_rows, n_cols), dtype=object)

        for i, row in enumerate(self.rows):
            for j, cell in enumerate(row):
                self.coos[i][j] = cell.get_center()
                self.left_coos[i][j] = cell.get_left()
                self.rigth_coos[i][j] = cell.get_right()

        self.texts = []
        if len(cell) == 2:
            for i, row in enumerate(table):
                row_texts = []
                for j, row in enumerate(n_rows):
                    a, b = row
                    a = Text(a).move_to( (self.rigth_coos[i][j]-self.left_coos[i][j])/3 + self.left_coos[i][j])
                    b = Text(b).move_to( 2*(self.rigth_coos[i][j]-self.left_coos[i][j])/3 + self.left_coos[i][j])
                    row_texts.append((a, b))
                self.texts.append(row_texts)
        else:
            for i, row in enumerate(table):
                for j, cell in row:
                    cell = Text(a).move_to(self.coos[i][j])

    def _set_header_coos(self, row_headers_cells, col_headers_cells):
        self.header_coos = np.empty((n_rows, n_cols), dtype=object)
        for i, row in enumerate(row_headers_cells):
            self.header_coos[0][i] = row.get_center()

        for i, col in enumerate(col_headers_cells):
            self.header_coos[1][i] = col.get_center()


    def _set_cell_coords(self):
        coos = np.empty((self.n_rows, self.n_cols), dtype=object)
        left_coos = np.empty((self.n_rows, self.n_cols), dtype=object)
        right_coos = np.empty((self.n_rows, self.n_cols), dtype=object)

        for i, row in enumerate(self.rows):
            for j, cell in enumerate(row):
                self.coos[i][j] = cell.get_center()
                self.left_coos[i][j] = cell.get_left()
                self.right_coos[i][j] = cell.get_right()

########################################################################
table_strs=[['0', '1'],['2', '3']]
row_headers=['a', 'b']
col_headers=['c', 'd']
table_width = TABLE_WIDTH
table_height = TABLE_HEIGHT
n_rows = 2
n_cols = 2

rows = [VGroup(*[Rectangle(width=table_width/(n_rows+1), height=table_height/(n_cols+1)) for cell in range(n_cols)]).arrange(buff = 0.0)]

for i in range(n_rows-1):
    rows.append(rows[0].copy().next_to(rows[0+i], DOWN, buff=0.0))

row_headers_cells = rows[0].copy().next_to(rows[0], UP, buff=0.0)
col_headers_cells = VGroup(*[row[0] for row in rows]).copy().next_to(rows[0][0], LEFT, buff=0.0).align_to(rows[0][0], UP)

table_body = VGroup(*rows, row_headers_cells, col_headers_cells).move_to(ORIGIN)

header_coos = np.empty((n_rows, n_cols), dtype=object)
for i, row in enumerate(row_headers_cells):
    header_coos[0][i] = row.get_center()

for i, col in enumerate(col_headers_cells):
    header_coos[1][i] = col.get_center()

row_headers_texts = [Text(text).move_to(header_coos[0][i]) for i, text in enumerate(row_headers)]
col_headers_texts = [Text(text).move_to(header_coos[1][i]) for i, text in enumerate(col_headers)]

coos = np.empty((n_rows, n_cols), dtype=object)
left_coos = np.empty((n_rows, n_cols), dtype=object)
rigth_coos = np.empty((n_rows, n_cols), dtype=object)


def _put_payoffs_in():
    texts = []
    for i, (row, row_str) in enumerate(zip(rows, table_strs)):
        for j, (cell, cell_strs) in enumerate(zip(row, row_str)):
            coos[i][j] = cell.get_center()
            left_coos[i][j] = cell.get_left()
            rigth_coos[i][j] = cell.get_right()
            # if len(cell_texts) == 2:
            cell_texts = []
            n_payoffs = len(cell_strs)
            payoff_space = (rigth_coos[i][j]-left_coos[i][j])/(n_payoffs+1)
            for k, cell_str in enumerate(cell_strs, 1):
                payoffs = []
                payoffs.append(Text(cell_str).move_to(left_coos[i][j] + k*payoff_space))
                cell_texts.append(tuple(*payoffs))
            texts.append(cell_texts)
    return(texts)
















        self.add(self.table)


    def get_cell_coos(self, row: int, col: int):
        return self.coos[row][col].get_center()
    
    
    def get_payoffs_coos(self, row: int, col: int):
        return [self.coos[row][col][i].get_center() for i in range(2)]

testos = GTtable([['0', '1'],
                  ['2', '3']],
                 row_headers=['a', 'b'],
                 col_headers=['c', 'd'])



DecimalTable
Table

class testos(Scene):
    def construct(self):
        table = GTtable()
        self.play(FadeIn(table))

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

        recall_prisoners_dilemma = Text('Let\'s recall prisoner\'s dilemma.')
        cooperation_and_altruism = Text('Cooperation and altruism').to_edge(UL)
        
        cell_m = Rectangle(width=TABLE_WIDTH/3, height=TABLE_HEIGHT/3)
        cell_r = Rectangle(width=TABLE_WIDTH/3, height=TABLE_HEIGHT/3).next_to(cell_m, RIGHT, buff=0.0)
        cell_l = Rectangle(width=TABLE_WIDTH/3, height=TABLE_HEIGHT/3).next_to(cell_m, LEFT, buff=0.0)
        mid_row = VGroup(cell_l, cell_m, cell_r)
        top_row = mid_row.copy().next_to(mid_row, UP, buff=0.0)
        bot_row = mid_row.copy().next_to(mid_row, DOWN, buff=0.0)
        table = VGroup(top_row, mid_row, bot_row).shift(UP)

        coos = np.empty((3, 3), dtype=object)
        for i, row in enumerate(table):
            for j, cell in enumerate(row):
                  coos[i][j] = cell.get_center()
        
        text_fight_col = Text('Fight').move_to(coos[0, 1])
        text_fight_row = Text('Fight').move_to(coos[1, 0])
        
        text_share_col = Text('Share').move_to(coos[0, 2])
        text_share_row = Text('Share').move_to(coos[2, 0])
        
        payoffs = [1, 1, 3, 0, 0, 3, 2, 2]
        payoffs_texts = [Text(str(payoff)) for payoff in payoffs]
        payoffs_fadein = payoffs.copy()
        payoffs_fadeout = payoffs.copy()
        
        # f_f_l = Text(str(payoffs[0])).move_to(coo[1,1]).shift(0.7*LEFT)
        # f_f_r = Text(str(payoffs[1])).move_to(coo[1,1]).shift(0.7*RIGHT)
        # f_s = Text(payoffs[1]).move_to(coo[1,2])
        # s_f = Text(payoffs[2]).move_to(coo[2,1])
        # s_s = Text(payoffs[3]).move_to(coo[2,2])
        
        lrud = [LEFT, RIGHT, UP, DOWN]
        for i, payoff in enumerate(payoffs_texts):
            payoffs_fadein[i] = FadeIn(payoff.move_to(coos[np.floor(i/4+1).astype(int), np.floor((i%4)/2).astype(int)+1]).shift(0.7*lrud[i % 2]))
            payoffs_fadeout[i] = FadeOut(payoff.move_to(coos[np.floor(i/4+1).astype(int), np.floor((i%4)/2).astype(int)+1]).shift(0.7*lrud[i % 2]))
        
        
        text_below_table = Text('Once again, Prisoner\'s dilemma is \"a reason why we can\'t have nice things.\"', font_size=28).next_to(table.get_bottom(), DOWN).shift(DOWN)
        
        self.play(Write(recall_prisoners_dilemma))
        self.play(FadeOut(recall_prisoners_dilemma))
        self.play(FadeIn(table))
        self.play(AnimationGroup(Write(text_fight_row), Write(text_share_row)))
        self.play(AnimationGroup(Write(text_fight_col), Write(text_share_col)))
        
        for i in range(4):
            self.play(AnimationGroup(*payoffs_fadein[2*i:2*i+2]))
        # self.play(FadeIn(f_f_l))
        # self.play(FadeIn(f_f_r))
        # self.play(FadeIn(f_s))
        # self.play(FadeIn(s_f))
        # self.play(FadeIn(s_s))
        self.play(Indicate(VGroup(*payoffs_texts[0], *payoffs_texts[2])))
        self.play(Indicate(VGroup(*payoffs_texts[1], *payoffs_texts[5])))
        self.wait()
        self.play(Write(text_below_table))
        self.play(AnimationGroup(*payoffs_fadeout, FadeOut(table), *[FadeOut(text) for text in payoffs_texts], FadeOut(text_fight_row)))
        self.play(Write(cooperation_and_altruism))
        
        
        # t = Table([['2      2', '0      3'],
        #            ['3      0', '1      1']],
        #           row_labels=[Text('Fight'), Text('Share')],
        #           col_labels=[Text('Fight'), Text('Share')],
        #           include_outer_lines=True).shift(UP)

        # t.get_horizontal_lines().set_color(DEF_COL)
        # t.get_vertical_lines().set_color(DEF_COL)
        # t.get_labels().set_color(DEF_COL)
        
        # t2 = t.copy()
        # for i in range(2, 4):
        #     t2.add_highlighted_cell((i, 2), color=TEAL_B)
        
        # self.play(t.create())
        
        # self.play(FadeIn(t2))
        # self.play(FadeOut(t2))

        # t3 = t.copy()
        # for i in range(2, 4):
        #     t3.add_highlighted_cell((2, i), color=TEAL_B)

        # self.play(FadeIn(t3))
        # self.play(FadeOut(t3))
        
        # t4 = t.copy()
        # t4.get_cell((2,2), color=YELLOW_C)

        # t = Table([['', ''],
        #            ['', '']],
        #           row_labels=[Text('Hawk meets'), Text('Dove meets')],
        #           col_labels=[Text('Hawk'), Text('Dove')],
        #           include_outer_lines=True).shift(UP)

        # cells = []
        # for i in range(2, 4):
        #     for j in range(2, 4):
        #         cells.append(t.get_cell((i,j)).get_center())
        
        # vals = t.get_entries()
        # vals.set_opacity(0)
        # labs = t.get_labels()
        # self.play(FadeIn(t))

        # for lab in labs:
        #     self.play(lab.animate.set_opacity(1))
        
        # value = MathTex('{{V}}').save_state()
        # cost = MathTex('{{C}}').save_state()
        # hawks = MathTex('{{H}}').save_state()
        # doves = MathTex('{{D}}').save_state()
        # value_desc = MathTex(r'\text{--- Value or payoff}').save_state()
        # cost_desc = MathTex(r'\text{--- Cost}').save_state()
        # hawks_desc = MathTex(r'\text{--- The proportion of hawks}').save_state()
        # doves_desc = MathTex(r'\text{--- The proportion of doves}').save_state()
        # one_minus_hawks = MathTex('1 - H').save_state()
        
        # value_desc.next_to(t, DOWN)
        # value.next_to(value_desc, LEFT)
        # cost.next_to(value, DOWN)
        # cost_desc.next_to(cost, RIGHT)
        
        # fight = MathTex('{', *division('{{V}}', '2'), '-', *division('{{C}}', '2'), '}').move_to(cells[0])
        # share = MathTex(*division('{{V}}', '2')).move_to(cells[3])
        # # fight = MathTex('{', '{', '{{V}}', r'\over', '2', '}', '-', '{', '{{C}}', r'\over', '2', '}', '}').move_to(cells[0])
        
        # self.play(Create(VGroup(value, value_desc)))
        # self.play(Create(VGroup(cost, cost_desc)))

        # self.play(TransformMatchingTex(VGroup(value.copy(), cost.copy()), fight))
        # self.play(value.copy().animate.move_to(cells[1]))
        # self.play(FadeIn(MathTex('0').move_to(cells[2])))
        # self.play(TransformMatchingTex(value.copy(), share))

        # # calc_eqs = []
        # # for i, calc in enumerate(calcs):
        # #     self.wait()
        # #     calc_eqs.append(MathTex(*calc).scale(DEF_SCALE).move_to([-4,3,0]))
        # #     if i == 0:
        # #         self.play(Create(*calc_eqs[i]))
        # #     else:
        # #         calc_eqs[i].next_to(calc_eqs[i-1], DOWN)
        # #         self.play(TransformMatchingTex(calc_eqs[i-1].copy(), calc_eqs[i]))
        # #         # self.play(TransformMatchingShapes(*calc_eqs[i:i+2]))
        

        self.wait(PAUSE)