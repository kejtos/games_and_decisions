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


class GTtable(VMobject):
    def __init__(self,
                 table: list[list[str]],
                 row_headers: list[str],
                 col_headers: list[str],
                 table_width: float = TABLE_WIDTH,
                 table_height: float = TABLE_HEIGHT,
                 rows: int = 2,
                 cols: int = 2,
                 **kwargs):
        # initialize the vmobject
        super().__init__(**kwargs)

        self.rows = []

        self.rows.append(VGroup(*[Rectangle(width=table_width/(rows+1), height=table_height/(cols+1)) for cell in range(cols)]).arrange(buff = 0.0))
        for i in range(rows-1):
            self.rows.append(self.rows[0].copy().next_to(self.rows[0+i], DOWN, buff=0.0))
        
        
            

        self.table = VGroup(*self.rows).move_to(ORIGIN)
        self.add(self.table)
        # coo = np.empty((3, 3), dtype=object)
        # for i, row in enumerate(table):
        #     for j, cell in enumerate(row):
        #           coo[i][j] = cell.get_center()

DecimalTable
class GTtable2(Table):
    def __init__(
        self,
        table: Iterable[Iterable[float | str | VMobject]],
        row_labels: Iterable[VMobject] | None = None,
        col_labels: Iterable[VMobject] | None = None,
        top_left_entry: VMobject | None = None,
        v_buff: float = 0.8,
        h_buff: float = 1.3,
        include_outer_lines: bool = False,
        add_background_rectangles_to_entries: bool = False,
        entries_background_color: Color = BLACK,
        include_background_rectangle: bool = False,
        background_rectangle_color: Color = BLACK,
        element_to_mobject: Callable[
            [float | str | VMobject],
            VMobject,
        ] = Paragraph,
        element_to_mobject_config: dict = {},
        arrange_in_grid_config: dict = {},
        line_config: dict = {},
        **kwargs,
        ):
        super().__init__(table: Iterable[Iterable[float | str | VMobject]],
                         row_labels: Iterable[VMobject] | None = None,
                         col_labels: Iterable[VMobject] | None = None,
                         top_left_entry: VMobject | None = None,
                         v_buff: float = 0.8,
                         h_buff: float = 1.3,
                         include_outer_lines: bool = False,
                         add_background_rectangles_to_entries: bool = False,
                         entries_background_color: Color = BLACK,
                         include_background_rectangle: bool = False,
                         background_rectangle_color: Color = BLACK,
                         element_to_mobject: Callable[
                             [float | str | VMobject],
                             VMobject,
                             ] = Paragraph,
                         element_to_mobject_config: dict = {},
                         arrange_in_grid_config: dict = {},
                         line_config: dict = {},
                         **kwargs,
                         ):
    
    def set_value(self):
        table


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

        coo = np.empty((3, 3), dtype=object)
        for i, row in enumerate(table):
            for j, cell in enumerate(row):
                  coo[i][j] = cell.get_center()
        
        text_fight_col = Text('Fight').move_to(coo[0, 1])
        text_fight_row = Text('Fight').move_to(coo[1, 0])
        
        text_share_col = Text('Share').move_to(coo[0, 2])
        text_share_row = Text('Share').move_to(coo[2, 0])
        
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
            payoffs_fadein[i] = FadeIn(payoff.move_to(coo[np.floor(i/4+1).astype(int), np.floor((i%4)/2).astype(int)+1]).shift(0.7*lrud[i % 2]))
            payoffs_fadeout[i] = FadeOut(payoff.move_to(coo[np.floor(i/4+1).astype(int), np.floor((i%4)/2).astype(int)+1]).shift(0.7*lrud[i % 2]))
        
        
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