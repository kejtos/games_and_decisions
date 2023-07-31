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
DECS = (2,0,0,2,0)

class Count(Animation):
    def __init__(self, number: DecimalNumber, start: float, end: float, **kwargs) -> None:
        super().__init__(number,  **kwargs)
        self.start = start
        self.end = end

    def interpolate_mobject(self, alpha: float) -> None:
        value = self.start + (alpha * (self.end - self.start))
        self.mobject.set_value(value)


class CreateBraess(Scene):
    def construct(self):
        trans_numbers = (N_TOP, N_TOP, N_BOT, N_BOT, 0)
        colors  = [MAROON_D, BLUE_D, BLUE_D, GREEN_D]
        rads = [0.8, 0.4, 0.4, 0.8]
        coords = ([-X_MOVE, 0, 0], [0, Y_MOVE, 0], [0, -Y_MOVE, 0], [X_MOVE, 0, 0])
        labels = ['Cars:', 'Time:']
        calcs =([r'{{\frac{N_a}{80}+45}} = {{45 + \frac{N_d}{120}}}'],
                [r'{ {{N_a}}', ' \over ', '{{80}} }', ' = ', '{ {{N_d}}', ' \over ', '{{120}} }'],
                [r'{ {{N_a}}', ' \over ', '{{80}} }', ' = ', '{ {{2000-N_a}}', ' \over ', '{{120}} }'],
                [r'{{120}} {{N_a}} = {{80}} ({{2000-N_a}})'],
                [r'{{120}} {{N_a}} = {{160000}} - {{80}} N_a'],
                [r'200 {{N_a}} = {{160000}}'],
                [r'{{N_a}} = 800'])

        cs = []
        for i, (col, rad, coord) in enumerate(zip(colors, rads, coords)):
            cs.append(Circle(radius=rad, color=col, arc_center=coord))
            cs[i].set_fill(col, opacity=OPACITY)

        c_st_p1 = cs[0].point_at_angle(np.arctan((-Y_MOVE)/(-X_MOVE)))
        c_top_p1 = cs[1].point_at_angle(PI+np.arctan((-Y_MOVE)/(-X_MOVE)))

        c_st_p2 = np.array([c_st_p1[0], -c_st_p1[1], c_st_p1[2]])
        c_bop_p1 = np.array([c_top_p1[0], -c_top_p1[1], c_top_p1[2]])

        c_top_p2 = np.array([-c_top_p1[0], c_top_p1[1], c_top_p1[2]])
        c_end_p1 = np.array([-c_st_p1[0], c_st_p1[1], c_st_p1[2]])

        c_bot_p2 = np.array([-c_bop_p1[0], c_bop_p1[1], c_bop_p1[2]])
        c_end_p2 = np.array([-c_st_p2[0], c_st_p2[1], c_st_p2[2]])

        ls = []
        ls.append(Line(c_st_p1, c_top_p1))
        ls.append(Line(c_top_p2, c_end_p1))
        ls.append(Line(c_st_p2, c_bop_p1))
        ls.append(Line(c_bot_p2, c_end_p2))
        ls.append(DashedLine(cs[1],cs[2]))

        eqs = []
        eqs.append(MathTex(r't_a = \frac{N_a}{80}').next_to(ls[0], LEFT, buff=0.5).shift(3*RIGHT+1.25*UP))
        eqs.append(MathTex(r't_b = 45').set_y(eqs[0].get_y()).set_x(-eqs[0].get_x()))
        eqs.append(MathTex(r't_c = 45').set_y(-eqs[0].get_y()).set_x(eqs[0].get_x()))
        eqs.append(MathTex(r't_d = \frac{N_d}{120}').set_y(-eqs[0].get_y()).set_x(-eqs[0].get_x()))
        eqs.append(MathTex(r't_e = 10').next_to(ls[4], RIGHT, buff=0.5))

        main_pic = VGroup(*cs, *ls[0:4], *eqs[0:4])
        main_pic.save_state()
        
        self.play(Create(cs[0]), Create(cs[3]))
        self.play(Create(cs[1]), Create(cs[2]))
        
        self.wait(PAUSE)
        
        self.play(Create(ls[0]), Create(ls[2]), run_time=0.75)
        self.play(Create(ls[1]), Create(ls[3]), run_time=0.75)
        
        self.wait(PAUSE)
        
        self.play(*[Write(eq) for eq in eqs[0:4]])

        self.wait(PAUSE)

        self.play(main_pic.animate.scale(DEF_SCALE).shift(1.5*DOWN+1.5*RIGHT))
        
        top_path = VGroup(cs[0].copy(), ls[0].copy(), cs[1].copy(), ls[1].copy(), cs[3].copy())
        bot_path = VGroup(cs[0].copy(), ls[2].copy(), cs[2].copy(), ls[3].copy(), cs[3].copy())

        self.wait(PAUSE)
        
        self.play(top_path.animate.scale(0.25).move_to([-5.5, 3.3, 0]))
        
        self.wait(PAUSE)
        
        eqtop = MathTex(r'{{\frac{N_a}{80}+45}}').scale(DEF_SCALE).next_to(top_path, RIGHT, buff=0.3)
        self.play(Write(eqtop))
        
        self.wait(PAUSE)
        
        self.play(bot_path.animate.scale(0.25).move_to([-5.5, 1.8, 0]))
        
        self.wait(PAUSE)
        
        eqbot = MathTex(r'{{45 + \frac{N_d}{120}}}').scale(DEF_SCALE).next_to(bot_path, RIGHT).align_to(eqtop, LEFT)
        self.play(Write(eqbot))
        
        eqtopbot = VGroup(eqtop, eqbot)
        
        calc_eqs = [eqtopbot.copy()]
        for i, calc in enumerate(calcs):
            self.wait(PAUSE)
            calc_eqs.append(MathTex(*calc).scale(DEF_SCALE).next_to(eqtopbot, RIGHT, buff=2.5))
            if i != 1:
                self.play(TransformMatchingTex(*calc_eqs[i:i+2]))
            else:
                self.play(TransformMatchingShapes(*calc_eqs[i:i+2]))

        calc_eqs.append(MathTex(r'{{N_d}} = 1200').scale(DEF_SCALE).next_to(eqtopbot, RIGHT, buff=2.5))
        self.play(AnimationGroup(calc_eqs[-2].animate.shift(UP*0.25), Write(calc_eqs[-1].shift(DOWN*0.25)), lag_ratio=0.5))
        
        self.wait(PAUSE)
        
        self.play(AnimationGroup(FadeOut(*calc_eqs[-2:], top_path, bot_path, eqbot, eqtop), Restore(main_pic), lag_ratio=0.2))
        
        self.wait(PAUSE)
        
        self.play(Create(ls[4]))
        
        self.wait(PAUSE)
        
        self.play(Write(eqs[4]))
        
        self.wait(PAUSE)
        
        ls.append(Line(*cs[1:3]))
        self.play(ReplacementTransform(*ls[4:6]))
        
        self.wait(PAUSE)
        
        self.play(FadeOut(*eqs))

        nums1 = []
        for time, n_dec in zip(TIMES, DECS):
            nums1.append(DecimalNumber(number=time, num_decimal_places=n_dec).scale(DEF_SCALE).set_color(WHITE))

        nums2 = []
        texts = []
        for i, num in enumerate(trans_numbers):
            nums2.append(DecimalNumber(number=num, num_decimal_places=0).scale(DEF_SCALE).set_color(WHITE))
            nums2[i].add_updater(lambda number: number).move_to(eqs[i]).shift(0.5*RIGHT)
            nums1[i].add_updater(lambda number: number).move_to(nums2[i]).shift(0.5*DOWN).align_to(nums2[i], LEFT)
            texts.append(Text(labels[0]).match_height(nums2[0]).next_to(nums2[i], LEFT).align_to(nums2[i], DOWN))
            texts.append(Text(labels[1]).match_height(nums2[0]).next_to(nums1[i], LEFT).align_to(nums1[i], DOWN))

        main_pic.add(eqs[4], ls[5])

        self.play(*[Create(text) for text in texts])

        self.wait(PAUSE)

        self.play(*[FadeIn(num) for num in nums1+nums2])

        self.wait(PAUSE)

        self.play(AnimationGroup(Count(nums1[0], N_TOP/DEN_TOP, N/DEN_TOP),
                                 Count(nums1[1], CONS_TOP, CONS_TOP),
                                 Count(nums1[2], CONS_BOT, CONS_BOT),
                                 Count(nums1[3], N_BOT/DEN_BOT, N/DEN_BOT),
                                 Count(nums1[4], 10, 10),
                                 Count(nums2[0], N_TOP, N),
                                 Count(nums2[1], N_TOP, 0),
                                 Count(nums2[2], N_BOT, 0),
                                 Count(nums2[3], N_BOT, N),
                                 Count(nums2[4], 0, N),
                                 ls[0].animate.set_color(RED),
                                 ls[1].animate.set_color(GREEN),
                                 ls[2].animate.set_color(GREEN),
                                 ls[3].animate.set_color(RED),
                                 ls[5].animate.set_color(RED)), run_time=10)

        self.wait(PAUSE)
        
        self.play(AnimationGroup(FadeOut(*nums1+nums2+texts)))
        self.play(AnimationGroup(FadeIn(*eqs)))
        self.play(main_pic.animate.scale(DEF_SCALE).shift(1.5*DOWN+1.5*RIGHT))
        
        self.wait(PAUSE)
        
        top_path = VGroup(cs[0].copy(), ls[0].copy(), cs[1].copy(), ls[1].copy(), cs[3].copy())
        bot_path = VGroup(cs[0].copy(), ls[2].copy(), cs[2].copy(), ls[3].copy(), cs[3].copy())
        all_path = VGroup(cs[0].copy(), ls[0].copy(), cs[1].copy(), ls[5].copy(), cs[2].copy(), ls[3].copy(), cs[3].copy())
        never_path = VGroup(cs[0].copy(), ls[2].copy(), cs[1].copy(), ls[5].copy(), cs[2].copy(), ls[1].copy(), cs[3].copy())

        self.play(top_path.animate.scale(0.25).move_to([-5.5, 3.3, 0]))
        eqtop = MathTex(r'25 + 45 = 70').scale(DEF_SCALE).next_to(top_path, RIGHT, buff=0.3)
        self.play(Write(eqtop))
        
        self.wait(PAUSE)
        
        self.play(bot_path.animate.scale(0.25).move_to([-5.5, 1.8, 0]))
        eqbot = MathTex(r'45 + 16.67 = 61.67').scale(DEF_SCALE).next_to(bot_path, RIGHT).align_to(eqtop, LEFT)
        self.play(Write(eqbot))
        
        self.wait(PAUSE)
        
        self.play(all_path.animate.scale(0.25).move_to([1, 3.3, 0]))

        self.wait(PAUSE)
        
        eqall = MathTex(r'25 + 10 + 16.67 = 51.67').scale(DEF_SCALE).next_to(all_path, RIGHT, buff=0.3)
        self.play(Write(eqall))
        
        self.wait(PAUSE)
        
        self.play(never_path.animate.scale(0.25).move_to([1, 1.8, 0]))
        
        self.wait(PAUSE)
        
        eqnever = MathTex(r'45 + 10 + 45 = 100').scale(DEF_SCALE).next_to(never_path, RIGHT).align_to(eqall, LEFT)
        self.play(Write(eqnever))
        
        self.wait(PAUSE)





