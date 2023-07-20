from manim import *
from manim.opengl import *
import numpy as np


class Count(Animation):
    def __init__(self, number: DecimalNumber, start: float, end: float, **kwargs) -> None:
        super().__init__(number,  **kwargs)
        self.start = start
        self.end = end

    def interpolate_mobject(self, alpha: float) -> None:
        value = self.start + (alpha * (self.end - self.start))
        self.mobject.set_value(value)

class CountingScene(Scene):
    def construct(self):
        # Create Decimal Number and add it to scene
        number = DecimalNumber(number=800, num_decimal_places=0).set_color(WHITE).scale(5)
        # Add an updater to keep the DecimalNumber centered as its value changes
        number.add_updater(lambda number: number.move_to(ORIGIN))

        self.add(number)

        self.wait()

        # Play the Count Animation to count from 0 to 100 in 4 seconds
        self.play(Count(number, 800, 2000), run_time=4, rate_func=linear)

        self.wait()


class CreateBraess(Scene):
    def construct(self):
        X_MOVE = 5.5
        Y_MOVE = 2
        PAUSE = 2

        c_start = Circle(radius=.8, color=MAROON_D, arc_center=np.array([-X_MOVE, 0., 0.]))
        c_start.set_fill(MAROON_D, opacity=.5)

        c_top = Circle(radius=.4, color=BLUE_D, arc_center=np.array([0., Y_MOVE, 0.]))
        c_top.set_fill(BLUE_D, opacity=.5)

        c_bot = Circle(radius=.4, color=BLUE_D, arc_center=np.array([0., -Y_MOVE, 0.]))
        c_bot.set_fill(BLUE_D, opacity=.5)

        c_end = Circle(radius=.8, color=GREEN_D, arc_center=np.array([X_MOVE, 0., 0.]))
        c_end.set_fill(GREEN_D, opacity=.5)


        c_st_p1 = c_start.point_at_angle(np.arctan((-Y_MOVE)/(-X_MOVE)))
        c_top_p1 = c_top.point_at_angle(PI+np.arctan((-Y_MOVE)/(-X_MOVE)))

        c_st_p2 = np.array([c_st_p1[0], -c_st_p1[1], c_st_p1[2]])
        c_bop_p1 = np.array([c_top_p1[0], -c_top_p1[1], c_top_p1[2]])

        c_top_p2 = np.array([-c_top_p1[0], c_top_p1[1], c_top_p1[2]])
        c_end_p1 = np.array([-c_st_p1[0], c_st_p1[1], c_st_p1[2]])

        c_bot_p2 = np.array([-c_bop_p1[0], c_bop_p1[1], c_bop_p1[2]])
        c_end_p2 = np.array([-c_st_p2[0], c_st_p2[1], c_st_p2[2]])

        la = Line(c_st_p1,c_top_p1)
        lb = Line(c_top_p2,c_end_p1)
        lc = Line(c_st_p2,c_bop_p1)
        ld = Line(c_bot_p2,c_end_p2)

        lmid = DashedLine(c_top,c_bot)
        
        
        eqa = MathTex(r't_a = \frac{N_a}{80}').next_to(la, LEFT, buff=0.5).shift(3*RIGHT+1.25*UP)
        eqb = MathTex(r't_b = 45').set_y(eqa.get_y()).set_x(-eqa.get_x())
        eqc = MathTex(r't_c = 45').set_y(-eqa.get_y()).set_x(eqa.get_x())
        eqd = MathTex(r't_d = \frac{N_d}{120}').set_y(-eqa.get_y()).set_x(-eqa.get_x())


        main_pic = VGroup(c_start, c_top, c_bot, c_end, la, lb, lc, ld, eqa, eqb, eqc, eqd)
        main_pic.save_state()
        
        self.play(Create(c_start), Create(c_end))
        self.play(Create(c_top), Create(c_bot))
        
        self.wait(PAUSE)
        
        self.play(Create(la), Create(lc), run_time=0.75)
        self.play(Create(lb), Create(ld), run_time=0.75)
        
        self.wait(PAUSE)
        
        self.play(Write(eqa), Write(eqb), Write(eqc), Write(eqd))

        self.wait(PAUSE)

        self.play(main_pic.animate.scale(0.75).shift(1.5*DOWN+1.5*RIGHT))
        
        top_path = VGroup(c_start.copy(), la.copy(), c_top.copy(), lb.copy(), c_end.copy())
        bot_path = VGroup(c_start.copy(), lc.copy(), c_bot.copy(), ld.copy(), c_end.copy())
        
        self.wait(PAUSE)
        
        self.play(top_path.animate.scale(0.25).move_to([-5.5,3.3,0]))
        eqtop = MathTex(r'{{\frac{N_a}{80}+45}}').next_to(top_path, RIGHT, buff=0.5).scale(0.75)
        
        self.wait(PAUSE)
        
        self.play(Write(eqtop))
        
        self.wait(PAUSE)
        
        self.play(bot_path.animate.scale(0.25).move_to([-5.5,2,0]))
        eqbot = MathTex(r'{{45 + \frac{N_d}{120}}}').next_to(bot_path, RIGHT, buff=0.5).scale(0.75)
        
        self.wait(PAUSE)
        
        self.play(Write(eqbot))
        
        self.wait(PAUSE)
        
        eqtopbot = VGroup(eqtop, eqbot)
        nash = MathTex(r'{{\frac{N_a}{80}+45}} = {{45 + \frac{N_d}{120}}}').next_to(eqtopbot, RIGHT, buff=2.5).scale(0.75)
        self.play(TransformMatchingTex(eqtopbot.copy(), nash))
        
        self.wait(PAUSE)
        
        nash2 = MathTex(r'{ {{N_a}}', ' \over ', '{{80}} }', ' = ', '{ {{N_d}}', ' \over ', '{{120}} }').next_to(eqtopbot, RIGHT, buff=2.5).scale(0.75)
        self.play(TransformMatchingShapes(nash, nash2))

        self.wait(PAUSE)
        nash3 = MathTex(r'{ {{N_a}}', ' \over ', '{{80}} }', ' = ', '{ {{2000-N_a}}', ' \over ', '{{120}} }').next_to(eqtopbot, RIGHT, buff=2.5).scale(0.75)
        self.play(TransformMatchingTex(nash2, nash3))
        
        self.wait(PAUSE)
        
        nash4 = MathTex(r'{{120}} {{N_a}} = {{80}} ({{2000-N_a}})').next_to(eqtopbot, RIGHT, buff=2.5).scale(0.75)
        self.play(TransformMatchingTex(nash3, nash4))
        
        self.wait(PAUSE)
        
        nash5 = MathTex(r'{{120}} {{N_a}} = {{160000}} - {{80}} N_a').next_to(eqtopbot, RIGHT, buff=2.5).scale(0.75)
        self.play(TransformMatchingTex(nash4, nash5))
        
        self.wait(PAUSE)
        
        nash6 = MathTex(r'200 {{N_a}} = {{160000}}').next_to(eqtopbot, RIGHT, buff=2.5).scale(0.75)
        self.play(TransformMatchingTex(nash5, nash6))
        
        self.wait(PAUSE)
        
        nash7 = MathTex(r'{{N_a}} = 800').next_to(eqtopbot, RIGHT, buff=2.5).scale(0.75)
        self.play(TransformMatchingTex(nash6, nash7))
        
        self.wait(PAUSE)
        
        nash8 = MathTex(r'{{N_d}} = 1200').next_to(eqtopbot, RIGHT, buff=2.5).scale(0.75)
        self.play(AnimationGroup(nash7.animate.shift(UP*0.25), Write(nash8.shift(DOWN*0.25)), lag_ratio=0.5))
        
        self.wait(PAUSE)
        
        self.play(AnimationGroup(FadeOut(nash7, nash8, top_path, bot_path, eqbot, eqtop), Restore(main_pic), lag_ratio=0.2))
        
        self.wait(PAUSE)
        
        eqe = MathTex(r't_e = 10').next_to(lmid, RIGHT, buff=0.5)
        self.play(Create(lmid))
        
        self.wait(PAUSE)
        
        self.play(Write(eqe))
        
        self.wait(PAUSE)
        
        lmid2 = Line(c_top,c_bot)
        self.play(ReplacementTransform(lmid, lmid2))
        
        self.wait(PAUSE)
        
        ls = VGroup(la, lb, lc, ld, lmid2)
        ls.save_state()
        
        self.wait(PAUSE)
        
        self.play(FadeOut(eqa, eqb, eqc, eqd, eqe))
        
        numbera = DecimalNumber(number=800/80, num_decimal_places=2).set_color(WHITE).scale(0.75)
        numberb = DecimalNumber(number=45, num_decimal_places=0).set_color(WHITE).scale(0.75)
        numberc = DecimalNumber(number=45, num_decimal_places=0).set_color(WHITE).scale(0.75)
        numberd = DecimalNumber(number=1200/120, num_decimal_places=2).set_color(WHITE).scale(0.75)
        numbere = DecimalNumber(number=10, num_decimal_places=0).set_color(WHITE).scale(0.75)
        
        numbera2 = DecimalNumber(number=800, num_decimal_places=0).set_color(WHITE).scale(0.75)
        numberb2 = DecimalNumber(number=800, num_decimal_places=0).set_color(WHITE).scale(0.75)
        numberc2 = DecimalNumber(number=1200, num_decimal_places=0).set_color(WHITE).scale(0.75)
        numberd2 = DecimalNumber(number=1200, num_decimal_places=0).set_color(WHITE).scale(0.75)
        numbere2 = DecimalNumber(number=0, num_decimal_places=0).set_color(WHITE).scale(0.75)
        
        numbera2.add_updater(lambda number: number).move_to(eqa)
        numberb2.add_updater(lambda number: number).move_to(eqb)
        numberc2.add_updater(lambda number: number).move_to(eqc)
        numberd2.add_updater(lambda number: number).move_to(eqd)
        numbere2.add_updater(lambda number: number).move_to(eqe)
        
        numbera.add_updater(lambda number: number).move_to(numbera2).shift(0.5*DOWN)
        numberb.add_updater(lambda number: number).move_to(numberb2).shift(0.5*DOWN)
        numberc.add_updater(lambda number: number).move_to(numberc2).shift(0.5*DOWN)
        numberd.add_updater(lambda number: number).move_to(numberd2).shift(0.5*DOWN)
        numbere.add_updater(lambda number: number).move_to(numbere2).shift(0.5*DOWN)
        
        main_pic.remove(eqa, eqb, eqc, eqd, eqe)
        main_pic.add(lmid2)
        
        self.play(Create(numbera), Create(numberb), Create(numberc), Create(numberd), Create(numbere), Create(numbera2), Create(numberb2), Create(numberc2), Create(numberd2), Create(numbere2))
        
        self.wait(PAUSE)
        
        self.play(AnimationGroup(Count(numbera, 800/80, 2000/80), Count(numberb, 45, 45), Count(numberc, 45, 45), Count(numberd, 1200/120, 2000/120), Count(numbere, 10, 10), Count(numbera2, 800, 2000), Count(numberb2, 800, 0), Count(numberc2, 1200, 0), Count(numberd2, 1200, 2000), Count(numbere2, 0, 2000),
                                 lc.animate.set_color(GREEN), lb.animate.set_color(GREEN), la.animate.set_color(RED), lmid2.animate.set_color(RED), ld.animate.set_color(RED)), run_time=10)
        
        self.wait(PAUSE)
        
        self.play(AnimationGroup(FadeOut(numbera), FadeOut(numberb), FadeOut(numberc), FadeOut(numberd), FadeOut(numbere), FadeOut(numbera2), FadeOut(numberb2),FadeOut(numberc2),FadeOut(numberd2), FadeOut(numbere2)))
        self.play(main_pic.animate.scale(0.75).shift(1.5*DOWN+1.5*RIGHT))
        
        self.wait(PAUSE)
        
        top_path = VGroup(c_start.copy(), la.copy(), c_top.copy(), lb.copy(), c_end.copy())
        bot_path = VGroup(c_start.copy(), lc.copy(), c_bot.copy(), ld.copy(), c_end.copy())
        good_path = VGroup(c_start.copy(), la.copy(), c_top.copy(), lmid2.copy(), c_bot.copy(), ld.copy(), c_end.copy())
        never_path = VGroup(c_start.copy(), lc.copy(), c_top.copy(), lmid2.copy(), c_bot.copy(), lb.copy(), c_end.copy())

        
        self.play(top_path.animate.scale(0.25).move_to([-5.5,3.3,0]))
        
        eqtop = MathTex(r'25 + 45 = 70').next_to(top_path, RIGHT, buff=0.3).scale(0.75)
        self.play(Write(eqtop))
        
        self.wait(PAUSE)
        
        self.play(bot_path.animate.scale(0.25).move_to([-5.67,2,0]))
        
        eqbot = MathTex(r'45 + 16.67 = 61.67').next_to(bot_path, RIGHT, buff=0.3).scale(0.75)
        self.play(Write(eqbot))
        
        self.wait(PAUSE)
        
        self.play(good_path.animate.scale(0.25).move_to([0.9,3.3,0]))
        
        self.wait(PAUSE)
        
        eqgood = MathTex(r'25 + 10 + 16.67 = 51.67').next_to(good_path, RIGHT, buff=0.3).scale(0.75)
        self.play(Write(eqgood))
        
        self.wait(PAUSE)
        
        self.play(never_path.animate.scale(0.25).move_to([1,2,0]))
        
        self.wait(PAUSE)
        
        eqnever = MathTex(r'45 + 10 + 45 = 100').next_to(never_path, RIGHT, buff=0.3).scale(0.75)
        self.play(Write(eqnever))
        
        self.wait(PAUSE)
        
        # self.wait(PAUSE)