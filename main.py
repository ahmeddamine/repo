from manim import *


class VideoLimites(Scene):
    """Vidéo: Limites d'une fonction — 1BAC SM (Maroc, BIOF)."""

    def construct(self):
        # SCENE 1
        self.scene_1_intro()
        # SCENE 2
        self.scene_2_notion_intuitive()
        # SCENE 3
        self.scene_3_gauche_droite()
        # SCENE 4
        self.scene_4_trou()
        # SCENE 5
        self.scene_5_definition_bac()
        # SCENE 6
        self.scene_6_proprietes_graphiques()
        # SCENE 7
        self.scene_7_limites_usuelles()
        # SCENE 8
        self.scene_8_forme_indeterminee()
        # SCENE 9
        self.scene_9_rationalisation()
        # SCENE 10
        self.scene_10_infini()
        # SCENE 11
        self.scene_11_pieges()
        # SCENE 12
        self.scene_12_exercices()
        # SCENE 13
        self.scene_13_resume()

    # ----------------------------
    # Outils utilitaires
    # ----------------------------
    def title_block(self, title_text, subtitle_text=None):
        title = Text(title_text, font_size=36, weight=BOLD, color=YELLOW).to_edge(UP)
        self.play(Write(title))
        subtitle = None
        if subtitle_text:
            subtitle = Text(subtitle_text, font_size=26, color=BLUE)
            subtitle.next_to(title, DOWN, buff=0.2)
            self.play(FadeIn(subtitle, shift=UP * 0.2))
        return title, subtitle

    def clear_scene(self, *mobs):
        self.play(*[FadeOut(mob) for mob in mobs if mob is not None])

    # ----------------------------
    # SCENE 1 — Intro
    # ----------------------------
    def scene_1_intro(self):
        title, subtitle = self.title_block(
            "Limites d’une fonction — 1BAC SM (Maroc)",
            "Définition • Propriétés • Méthodes • +∞/−∞ • Exercices",
        )

        axes = Axes(
            x_range=[-3, 4, 1],
            y_range=[-1, 5, 1],
            x_length=7,
            y_length=3.8,
            tips=False,
            axis_config={"include_numbers": True, "font_size": 20},
        ).to_edge(DOWN, buff=0.4)
        curve = axes.plot(lambda x: 0.5 * x + 1, x_range=[-2.8, 3.8], color=GREEN)

        self.play(Create(axes), Create(curve), run_time=1.8)
        self.wait(0.8)
        self.clear_scene(title, subtitle, axes, curve)

    # ----------------------------
    # SCENE 2 — Notion intuitive
    # ----------------------------
    def scene_2_notion_intuitive(self):
        title, _ = self.title_block("Notion intuitive de limite", "Exemple: f(x)=0.5x+1, a=2")

        axes = Axes(
            x_range=[-1, 5, 1],
            y_range=[0, 4, 1],
            x_length=8,
            y_length=4.2,
            tips=False,
            axis_config={"include_numbers": True, "font_size": 22},
        ).to_edge(DOWN, buff=0.45)
        graph = axes.plot(lambda x: 0.5 * x + 1, x_range=[-1, 5], color=BLUE)

        a = 2
        L = 0.5 * a + 1
        band = Rectangle(width=0.9, height=4.1, stroke_width=0, fill_color=YELLOW, fill_opacity=0.15)
        band.move_to(axes.c2p(a, 2))

        tracker = ValueTracker(-0.5)

        x_dot = always_redraw(lambda: Dot(axes.c2p(tracker.get_value(), 0), color=ORANGE))
        m_dot = always_redraw(
            lambda: Dot(axes.c2p(tracker.get_value(), 0.5 * tracker.get_value() + 1), color=RED)
        )
        v_line = always_redraw(
            lambda: DashedLine(
                axes.c2p(tracker.get_value(), 0),
                axes.c2p(tracker.get_value(), 0.5 * tracker.get_value() + 1),
                color=GRAY_B,
            )
        )
        h_line = always_redraw(
            lambda: DashedLine(
                axes.c2p(0, 0.5 * tracker.get_value() + 1),
                axes.c2p(tracker.get_value(), 0.5 * tracker.get_value() + 1),
                color=GRAY_B,
            )
        )

        a_line = DashedLine(axes.c2p(a, 0), axes.c2p(a, L), color=YELLOW)
        l_line = DashedLine(axes.c2p(0, L), axes.c2p(a, L), color=YELLOW)
        labels = VGroup(
            MathTex(r"a=2", font_size=30).next_to(axes.c2p(a, 0), DOWN),
            MathTex(r"L=2", font_size=30, color=RED).next_to(axes.c2p(0, L), LEFT),
        )

        formula = MathTex(r"\lim_{x\to 2} f(x)=2", font_size=42).to_corner(UR).shift(DOWN * 0.5)
        phrase = MathTex(
            r"\text{Quand }x\text{ s'approche de }2,\ f(x)\text{ s'approche de }L.",
            font_size=32,
        ).next_to(formula, DOWN, aligned_edge=RIGHT)

        self.play(Create(axes), Create(graph), FadeIn(band), run_time=1.6)
        self.play(Create(a_line), Create(l_line), Write(labels))
        self.play(FadeIn(x_dot), FadeIn(m_dot), Create(v_line), Create(h_line))
        self.play(tracker.animate.set_value(1.95), run_time=2.0, rate_func=linear)
        self.play(tracker.animate.set_value(2.05), run_time=1.4, rate_func=linear)
        self.play(Write(formula), FadeIn(phrase, shift=UP * 0.2))
        self.wait(0.6)

        self.clear_scene(title, axes, graph, band, a_line, l_line, labels, x_dot, m_dot, v_line, h_line, formula, phrase)

    # ----------------------------
    # SCENE 3 — Gauche / droite
    # ----------------------------
    def scene_3_gauche_droite(self):
        title, _ = self.title_block("Limite à gauche et à droite", "Fonction en escalier autour de 0")

        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[0, 4, 1],
            x_length=8,
            y_length=4,
            tips=False,
            axis_config={"include_numbers": True, "font_size": 22},
        ).to_edge(DOWN, buff=0.45)

        left_graph = axes.plot(lambda x: 1, x_range=[-3, -0.02], color=BLUE)
        right_graph = axes.plot(lambda x: 3, x_range=[0.02, 3], color=GREEN)
        x0_line = DashedLine(axes.c2p(0, 0), axes.c2p(0, 3.4), color=YELLOW)

        tracker = ValueTracker(-2.5)

        def step_value(x):
            return 1 if x < 0 else 3

        x_dot = always_redraw(lambda: Dot(axes.c2p(tracker.get_value(), 0), color=ORANGE))
        m_dot = always_redraw(lambda: Dot(axes.c2p(tracker.get_value(), step_value(tracker.get_value())), color=RED))
        segment = always_redraw(
            lambda: DashedLine(
                axes.c2p(tracker.get_value(), 0),
                axes.c2p(tracker.get_value(), step_value(tracker.get_value())),
                color=GRAY_B,
            )
        )

        left_lim = MathTex(r"\lim_{x\to 0^-} f(x)=1", font_size=38, color=BLUE).to_corner(UL).shift(DOWN * 0.6)
        right_lim = MathTex(r"\lim_{x\to 0^+} f(x)=3", font_size=38, color=GREEN).next_to(left_lim, DOWN, aligned_edge=LEFT)
        conclusion = MathTex(
            r"1\neq 3\ \Rightarrow\ \lim_{x\to0}f(x)\ \text{n'existe pas}",
            font_size=36,
            color=RED,
        ).to_edge(RIGHT).shift(UP * 0.2)

        self.play(Create(axes), Create(left_graph), Create(right_graph), Create(x0_line), run_time=1.6)
        self.play(FadeIn(x_dot), FadeIn(m_dot), Create(segment))

        self.play(tracker.animate.set_value(-0.08), run_time=1.8, rate_func=linear)
        self.play(Write(left_lim))

        self.play(tracker.animate.set_value(2.2), run_time=0.4)
        self.play(tracker.animate.set_value(0.08), run_time=1.8, rate_func=linear)
        self.play(Write(right_lim))

        self.play(Write(conclusion))
        self.wait(0.6)
        self.clear_scene(title, axes, left_graph, right_graph, x0_line, x_dot, m_dot, segment, left_lim, right_lim, conclusion)

    # ----------------------------
    # SCENE 4 — Trou
    # ----------------------------
    def scene_4_trou(self):
        title, _ = self.title_block("Cas du trou: limite existe mais f(a) non définie", "f(x)=\frac{x^2-1}{x-1},\ Df: x\neq1")

        axes = Axes(
            x_range=[-1, 4, 1],
            y_range=[-1, 5, 1],
            x_length=8,
            y_length=4,
            tips=False,
            axis_config={"include_numbers": True, "font_size": 22},
        ).to_edge(DOWN, buff=0.45)

        # f(x)=x+1 sauf en x=1
        g1 = axes.plot(lambda x: x + 1, x_range=[-1, 0.98], color=BLUE)
        g2 = axes.plot(lambda x: x + 1, x_range=[1.02, 4], color=BLUE)
        hole = Circle(radius=0.08, color=RED, stroke_width=3).move_to(axes.c2p(1, 2))

        tracker = ValueTracker(-0.5)
        m_dot = always_redraw(lambda: Dot(axes.c2p(tracker.get_value(), tracker.get_value() + 1), color=ORANGE))
        x_dot = always_redraw(lambda: Dot(axes.c2p(tracker.get_value(), 0), color=ORANGE))
        guide = always_redraw(
            lambda: DashedLine(axes.c2p(tracker.get_value(), 0), axes.c2p(tracker.get_value(), tracker.get_value() + 1), color=GRAY)
        )

        formula = MathTex(r"\lim_{x\to1}\frac{x^2-1}{x-1}=2", font_size=42).to_corner(UR).shift(DOWN * 0.5)
        df = MathTex(r"Df:\ x\neq1", font_size=34, color=YELLOW).next_to(formula, DOWN, aligned_edge=LEFT)
        phrase = MathTex(r"\text{La limite peut exister même si }f(1)\text{ n'existe pas.}", font_size=30).next_to(df, DOWN, aligned_edge=LEFT)

        self.play(Create(axes), Create(g1), Create(g2), Create(hole), run_time=1.6)
        self.play(FadeIn(x_dot), FadeIn(m_dot), Create(guide))
        self.play(tracker.animate.set_value(0.95), run_time=1.8, rate_func=linear)
        self.play(tracker.animate.set_value(1.6), run_time=0.5)
        self.play(tracker.animate.set_value(1.05), run_time=1.6, rate_func=linear)
        self.play(Write(formula), Write(df), FadeIn(phrase, shift=UP * 0.2))
        self.wait(0.6)

        self.clear_scene(title, axes, g1, g2, hole, x_dot, m_dot, guide, formula, df, phrase)

    # ----------------------------
    # SCENE 5 — Définition bac
    # ----------------------------
    def scene_5_definition_bac(self):
        title, _ = self.title_block("Définition (niveau bac)")

        main_formula = MathTex(r"\lim_{x\to a}f(x)=L", font_size=72)
        phrase = MathTex(r"x\ \text{proche de}\ a\ \Rightarrow\ f(x)\ \text{proche de}\ L", font_size=42)
        left_right = MathTex(r"\text{Rappel: vérifier la gauche et la droite.}", font_size=32, color=BLUE)

        block = VGroup(main_formula, phrase, left_right).arrange(DOWN, buff=0.45)
        frame = SurroundingRectangle(block, buff=0.35, color=BLUE)

        self.play(Write(main_formula))
        self.play(FadeIn(phrase, shift=UP * 0.2))
        self.play(Write(left_right), Create(frame))
        self.wait(0.8)

        self.clear_scene(title, block, frame)

    # ----------------------------
    # SCENE 6 — Propriétés + graphes
    # ----------------------------
    def scene_6_proprietes_graphiques(self):
        title, _ = self.title_block("Propriétés de calcul + interprétation graphique")

        table = VGroup(
            MathTex(r"\text{(a) }\lim(f+g)=\lim f+\lim g", font_size=32),
            MathTex(r"\text{(b) }\lim(f-g)=\lim f-\lim g", font_size=32),
            MathTex(r"\text{(c) }\lim(kf)=k\lim f", font_size=32),
            MathTex(r"\text{(d) }\lim(fg)=(\lim f)(\lim g)", font_size=32),
            MathTex(r"\text{(e) }\lim\!\left(\frac{f}{g}\right)=\frac{\lim f}{\lim g},\ \text{si }\lim g\neq0", font_size=32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).scale(0.95)
        table_box = SurroundingRectangle(table, buff=0.25, color=GRAY_B)
        table_group = VGroup(table_box, table).to_edge(LEFT).shift(DOWN * 0.35)

        axes = Axes(
            x_range=[-1, 4, 1],
            y_range=[-1, 6, 1],
            x_length=6.2,
            y_length=4.2,
            tips=False,
            axis_config={"include_numbers": True, "font_size": 18},
        ).to_edge(RIGHT, buff=0.35).shift(DOWN * 0.3)

        self.play(FadeIn(table_group), Create(axes))

        # (a) Somme: f=x, g=2, h=x+2
        tracker = ValueTracker(0.5)
        f = axes.plot(lambda x: x, x_range=[-1, 4], color=BLUE)
        g = axes.plot(lambda x: 2, x_range=[-1, 4], color=GREEN)
        h = axes.plot(lambda x: x + 2, x_range=[-1, 4], color=RED)
        dots_a = VGroup(
            always_redraw(lambda: Dot(axes.c2p(tracker.get_value(), tracker.get_value()), color=BLUE)),
            always_redraw(lambda: Dot(axes.c2p(tracker.get_value(), 2), color=GREEN)),
            always_redraw(lambda: Dot(axes.c2p(tracker.get_value(), tracker.get_value() + 2), color=RED)),
        )
        tag_a = MathTex(r"a)\ f=x,\ g=2,\ h=f+g", font_size=26).next_to(axes, UP)

        self.play(Indicate(table[0], color=YELLOW), Create(f), Create(g), Create(h), Write(tag_a), FadeIn(dots_a))
        self.play(tracker.animate.set_value(2), run_time=1.2, rate_func=linear)
        self.play(FadeOut(f), FadeOut(g), FadeOut(h), FadeOut(dots_a), FadeOut(tag_a))

        # (b) Différence: f=x+1, g=x, h=1
        tracker.set_value(0.5)
        f = axes.plot(lambda x: x + 1, x_range=[-1, 4], color=BLUE)
        g = axes.plot(lambda x: x, x_range=[-1, 4], color=GREEN)
        h = axes.plot(lambda x: 1, x_range=[-1, 4], color=RED)
        dots_b = VGroup(
            always_redraw(lambda: Dot(axes.c2p(tracker.get_value(), tracker.get_value() + 1), color=BLUE)),
            always_redraw(lambda: Dot(axes.c2p(tracker.get_value(), tracker.get_value()), color=GREEN)),
            always_redraw(lambda: Dot(axes.c2p(tracker.get_value(), 1), color=RED)),
        )
        sep = always_redraw(
            lambda: DashedLine(
                axes.c2p(tracker.get_value(), tracker.get_value()),
                axes.c2p(tracker.get_value(), tracker.get_value() + 1),
                color=YELLOW,
            )
        )
        tag_b = MathTex(r"b)\ h=f-g=1", font_size=26).next_to(axes, UP)

        self.play(Indicate(table[1], color=YELLOW), Create(f), Create(g), Create(h), Write(tag_b), FadeIn(dots_b), Create(sep))
        self.play(tracker.animate.set_value(2.3), run_time=1.2, rate_func=linear)
        self.play(FadeOut(f), FadeOut(g), FadeOut(h), FadeOut(dots_b), FadeOut(sep), FadeOut(tag_b))

        # (c) kf: f=x, h=2x
        tracker.set_value(0.2)
        f = axes.plot(lambda x: x, x_range=[-1, 3], color=BLUE)
        h = axes.plot(lambda x: 2 * x, x_range=[-1, 3], color=RED)
        dots_c = VGroup(
            always_redraw(lambda: Dot(axes.c2p(tracker.get_value(), tracker.get_value()), color=BLUE)),
            always_redraw(lambda: Dot(axes.c2p(tracker.get_value(), 2 * tracker.get_value()), color=RED)),
        )
        tag_c = MathTex(r"c)\ k=2\Rightarrow h=2f", font_size=26).next_to(axes, UP)

        self.play(Indicate(table[2], color=YELLOW), Create(f), Create(h), Write(tag_c), FadeIn(dots_c))
        self.play(tracker.animate.set_value(2.0), run_time=1.2, rate_func=linear)
        self.play(FadeOut(f), FadeOut(h), FadeOut(dots_c), FadeOut(tag_c))

        # (d) produit: f=x, g=x => h=x^2
        tracker.set_value(0.5)
        f = axes.plot(lambda x: x, x_range=[-1, 3], color=BLUE)
        h = axes.plot(lambda x: x**2, x_range=[-1, 3], color=RED)
        dots_d = VGroup(
            always_redraw(lambda: Dot(axes.c2p(tracker.get_value(), tracker.get_value()), color=BLUE)),
            always_redraw(lambda: Dot(axes.c2p(tracker.get_value(), tracker.get_value() ** 2), color=RED)),
        )
        tag_d = MathTex(r"d)\ h=f\cdot g=x^2,\ a=2", font_size=26).next_to(axes, UP)

        self.play(Indicate(table[3], color=YELLOW), Create(f), Create(h), Write(tag_d), FadeIn(dots_d))
        self.play(tracker.animate.set_value(2), run_time=1.2, rate_func=linear)
        self.play(FadeOut(f), FadeOut(h), FadeOut(dots_d), FadeOut(tag_d))

        # (e) quotient: f=x^2-1, g=x+1, h=x-1 (x!=-1), a=1
        tracker.set_value(-0.2)
        num = axes.plot(lambda x: x**2 - 1, x_range=[-1, 3], color=BLUE)
        den = axes.plot(lambda x: x + 1, x_range=[-1, 3], color=GREEN)
        q = axes.plot(lambda x: x - 1, x_range=[-0.95, 3], color=RED)
        dots_e = VGroup(
            always_redraw(lambda: Dot(axes.c2p(tracker.get_value(), tracker.get_value() ** 2 - 1), color=BLUE)),
            always_redraw(lambda: Dot(axes.c2p(tracker.get_value(), tracker.get_value() + 1), color=GREEN)),
            always_redraw(lambda: Dot(axes.c2p(tracker.get_value(), tracker.get_value() - 1), color=RED)),
        )
        cond = MathTex(r"\text{Condition: }\lim g\neq0\ \text{et Df: }x\neq-1", font_size=24, color=YELLOW)
        cond.next_to(axes, DOWN, buff=0.2)
        tag_e = MathTex(r"e)\ h=\frac{f}{g}=x-1\ (x\neq-1),\ a=1", font_size=25).next_to(axes, UP)

        self.play(Indicate(table[4], color=YELLOW), Create(num), Create(den), Create(q), Write(tag_e), FadeIn(dots_e), Write(cond))
        self.play(tracker.animate.set_value(1), run_time=1.3, rate_func=linear)
        self.wait(0.3)

        self.clear_scene(title, table_group, axes, num, den, q, dots_e, cond, tag_e)

    # ----------------------------
    # SCENE 7 — Limites usuelles
    # ----------------------------
    def scene_7_limites_usuelles(self):
        title, _ = self.title_block("Limites usuelles (avec mini-graphes)")

        cards = VGroup(
            MathTex(r"\lim_{x\to a}c=c", font_size=34),
            MathTex(r"\lim_{x\to a}x=a", font_size=34),
            MathTex(r"\lim_{x\to a}x^n=a^n", font_size=34),
            MathTex(r"\lim_{x\to a}\frac{1}{x}=\frac{1}{a}\ (a\neq0)", font_size=34),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(LEFT).shift(DOWN * 0.3)
        box = SurroundingRectangle(cards, buff=0.25, color=BLUE)

        axes = Axes(
            x_range=[-2, 3, 1],
            y_range=[-1, 4, 1],
            x_length=6.4,
            y_length=4,
            tips=False,
            axis_config={"include_numbers": True, "font_size": 18},
        ).to_edge(RIGHT, buff=0.4).shift(DOWN * 0.3)

        tracker = ValueTracker(-1.5)
        graph = axes.plot(lambda x: x**2, x_range=[-1.8, 2.2], color=GREEN)
        dot = always_redraw(lambda: Dot(axes.c2p(tracker.get_value(), tracker.get_value() ** 2), color=RED))

        self.play(FadeIn(box), Write(cards), Create(axes), Create(graph), FadeIn(dot))
        self.play(tracker.animate.set_value(1), run_time=1.8, rate_func=linear)
        self.wait(0.4)

        df_note = MathTex(r"Df\ \text{et conditions: ex. dénominateur}\neq0", font_size=30, color=YELLOW)
        df_note.to_edge(DOWN)
        self.play(Write(df_note))
        self.wait(0.5)

        self.clear_scene(title, box, cards, axes, graph, dot, df_note)

    # ----------------------------
    # SCENE 8 — 0/0 et simplification
    # ----------------------------
    def scene_8_forme_indeterminee(self):
        title, _ = self.title_block("Forme indéterminée 0/0 et simplification")

        axes = Axes(
            x_range=[-1, 5, 1],
            y_range=[0, 6, 1],
            x_length=8,
            y_length=4,
            tips=False,
            axis_config={"include_numbers": True, "font_size": 20},
        ).to_edge(DOWN, buff=0.45)

        # courbe avec trou: y=x+2 sauf x=2
        g1 = axes.plot(lambda x: x + 2, x_range=[-1, 1.95], color=BLUE)
        g2 = axes.plot(lambda x: x + 2, x_range=[2.05, 5], color=BLUE)
        hole = Circle(radius=0.08, color=RED).move_to(axes.c2p(2, 4))

        tracker = ValueTracker(0.0)
        dot = always_redraw(lambda: Dot(axes.c2p(tracker.get_value(), tracker.get_value() + 2), color=ORANGE))

        steps = VGroup(
            MathTex(r"\lim_{x\to2}\frac{x^2-4}{x-2}", font_size=38),
            MathTex(r"=\lim_{x\to2}\frac{(x-2)(x+2)}{x-2}", font_size=38),
            MathTex(r"=\lim_{x\to2}(x+2)=4", font_size=38, color=GREEN),
            MathTex(r"\text{Idée: }0/0\Rightarrow\text{factoriser et simplifier.}", font_size=30, color=YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(UL).shift(DOWN * 0.5)
        steps_box = SurroundingRectangle(steps, buff=0.2, color=GRAY_B)

        self.play(Create(axes), Create(g1), Create(g2), Create(hole), FadeIn(dot), run_time=1.6)
        self.play(tracker.animate.set_value(1.9), run_time=1.6, rate_func=linear)
        self.play(tracker.animate.set_value(2.1), run_time=0.6)
        self.play(tracker.animate.set_value(2.02), run_time=1.2, rate_func=linear)
        self.play(FadeIn(steps_box), Write(steps), run_time=2.0)
        self.wait(0.5)

        self.clear_scene(title, axes, g1, g2, hole, dot, steps, steps_box)

    # ----------------------------
    # SCENE 9 — Rationalisation
    # ----------------------------
    def scene_9_rationalisation(self):
        title, _ = self.title_block("Rationalisation (racines)", "Exemple: (√(x+4)-2)/x, x→0")

        axes = Axes(
            x_range=[-1, 3, 1],
            y_range=[0, 1.2, 0.2],
            x_length=7.5,
            y_length=4,
            tips=False,
            axis_config={"include_numbers": True, "font_size": 18},
        ).to_edge(DOWN, buff=0.45)

        # h(x) = (sqrt(x+4)-2)/x = 1/(sqrt(x+4)+2), x != 0
        left = axes.plot(lambda x: 1 / ((x + 4) ** 0.5 + 2), x_range=[-0.95, -0.03], color=BLUE)
        right = axes.plot(lambda x: 1 / ((x + 4) ** 0.5 + 2), x_range=[0.03, 3], color=BLUE)
        hole = Circle(radius=0.06, color=RED).move_to(axes.c2p(0, 0.25))

        tracker = ValueTracker(-0.8)
        dot = always_redraw(
            lambda: Dot(
                axes.c2p(tracker.get_value(), 1 / ((tracker.get_value() + 4) ** 0.5 + 2)),
                color=ORANGE,
            )
        )

        calc = VGroup(
            MathTex(r"\lim_{x\to0}\frac{\sqrt{x+4}-2}{x}\ \to\ \frac{0}{0}", font_size=34),
            MathTex(r"\times\frac{\sqrt{x+4}+2}{\sqrt{x+4}+2}", font_size=34),
            MathTex(r"\Rightarrow\ \frac{1}{\sqrt{x+4}+2}", font_size=34),
            MathTex(r"\lim_{x\to0}\frac{1}{\sqrt{x+4}+2}=\frac14", font_size=36, color=GREEN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_corner(UL).shift(DOWN * 0.45)

        self.play(Create(axes), Create(left), Create(right), Create(hole), FadeIn(dot), run_time=1.6)
        self.play(tracker.animate.set_value(-0.06), run_time=1.7, rate_func=linear)
        self.play(tracker.animate.set_value(1.0), run_time=0.6)
        self.play(tracker.animate.set_value(0.06), run_time=1.4, rate_func=linear)
        self.play(Write(calc), run_time=2.0)
        self.wait(0.5)

        self.clear_scene(title, axes, left, right, hole, dot, calc)

    # ----------------------------
    # SCENE 10 — +∞ et -∞
    # ----------------------------
    def scene_10_infini(self):
        title, _ = self.title_block("Limites en +∞ et −∞")

        left_axes = Axes(
            x_range=[-1, 5, 1],
            y_range=[-1, 20, 5],
            x_length=5.8,
            y_length=3.8,
            tips=False,
            axis_config={"include_numbers": True, "font_size": 16},
        ).to_edge(LEFT, buff=0.4).shift(DOWN * 0.45)
        poly = left_axes.plot(lambda x: x**2, x_range=[-1, 4.4], color=BLUE)
        arr = Arrow(start=left_axes.c2p(4.1, 16), end=left_axes.c2p(4.4, 19), color=YELLOW)
        poly_txt = MathTex(r"x\to+\infty\Rightarrow x^2\to+\infty", font_size=28).next_to(left_axes, UP)

        right_axes = Axes(
            x_range=[-2, 10, 2],
            y_range=[1, 6, 1],
            x_length=5.8,
            y_length=3.8,
            tips=False,
            axis_config={"include_numbers": True, "font_size": 16},
        ).to_edge(RIGHT, buff=0.4).shift(DOWN * 0.45)

        rat = right_axes.plot(lambda x: (3 * x**2 + 1) / (x**2 - 5 * x), x_range=[6, 10], color=GREEN)
        asym = right_axes.plot(lambda x: 3, x_range=[-2, 10], color=RED)
        formula = VGroup(
            MathTex(r"\lim_{x\to+\infty}\frac{3x^2+1}{x^2-5x}", font_size=30),
            MathTex(r"=\lim_{x\to+\infty}\frac{3+\frac{1}{x^2}}{1-\frac{5}{x}}=\frac{3}{1}=3", font_size=30, color=GREEN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(right_axes, UP)

        self.play(Create(left_axes), Create(poly), Write(poly_txt), GrowArrow(arr), run_time=1.8)
        self.play(Create(right_axes), Create(rat), Create(asym), Write(formula), run_time=2.0)
        self.wait(0.7)

        self.clear_scene(title, left_axes, poly, poly_txt, arr, right_axes, rat, asym, formula)

    # ----------------------------
    # SCENE 11 — Pièges
    # ----------------------------
    def scene_11_pieges(self):
        title, _ = self.title_block("Pièges fréquents")

        cards = [
            MathTex(r"\text{Piège 1: division par }0", font_size=44, color=RED),
            MathTex(r"\text{Piège 2: confondre limite et }f(a)", font_size=42, color=ORANGE),
            MathTex(r"\text{Piège 3: oublier }\lim g\neq0", font_size=42, color=RED_D),
        ]

        for card in cards:
            box = SurroundingRectangle(card, buff=0.2, color=GRAY_B)
            self.play(FadeIn(card, scale=1.05), Create(box), run_time=0.7)
            self.wait(0.4)
            self.play(FadeOut(card), FadeOut(box), run_time=0.45)

        self.clear_scene(title)

    # ----------------------------
    # SCENE 12 — Exercices
    # ----------------------------
    def scene_12_exercices(self):
        title, _ = self.title_block("Exercices finaux + correction animée")

        ex1 = MathTex(r"\text{Ex1: }\lim_{x\to2}\frac{x^2-4}{x-2}\ ?", font_size=40)
        ex2 = MathTex(r"\text{Ex2: }\lim_{x\to+\infty}\frac{3x^2+1}{x^2-5x}\ ?", font_size=40)
        exs = VGroup(ex1, ex2).arrange(DOWN, aligned_edge=LEFT, buff=0.5).to_edge(UP).shift(DOWN * 1.5)

        pause = Text("Pause 3 secondes pour chercher...", font_size=28, color=BLUE).to_edge(DOWN)
        self.play(Write(exs), FadeIn(pause))
        self.wait(3)

        corr1 = MathTex(
            r"\text{Ex1: }\frac{x^2-4}{x-2}=\frac{(x-2)(x+2)}{x-2}=x+2\Rightarrow\lim=4",
            font_size=30,
            color=GREEN,
        )
        corr2 = MathTex(
            r"\text{Ex2: }\lim\frac{3x^2+1}{x^2-5x}=\lim\frac{3+1/x^2}{1-5/x}=3",
            font_size=30,
            color=GREEN,
        )
        corr = VGroup(corr1, corr2).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(exs, DOWN, buff=0.7)

        self.play(FadeOut(pause), Write(corr), run_time=2.0)
        self.wait(0.7)

        self.clear_scene(title, exs, corr)

    # ----------------------------
    # SCENE 13 — Résumé
    # ----------------------------
    def scene_13_resume(self):
        title, _ = self.title_block("Résumé — À retenir")

        recap = VGroup(
            MathTex(r"\bullet\ \lim_{x\to a}f(x)=L\ \Leftrightarrow\ x\text{ proche de }a\Rightarrow f(x)\text{ proche de }L", font_size=28),
            MathTex(r"\bullet\ \text{Comparer gauche et droite}", font_size=28),
            MathTex(r"\bullet\ \text{Propriétés: somme, différence, }k\!f,\ produit,\ quotient\ (\lim g\neq0)", font_size=28),
            MathTex(r"\bullet\ 0/0\Rightarrow\text{factoriser / simplifier}", font_size=28),
            MathTex(r"\bullet\ \text{Racines: rationalisation (conjugué)}", font_size=28),
            MathTex(r"\bullet\ x\to\pm\infty:\ \text{comparer les degrés}", font_size=28),
            MathTex(r"\bullet\ \text{Toujours vérifier }Df\ \text{et les conditions}", font_size=28, color=YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).scale(0.95).next_to(title, DOWN, buff=0.35)

        box = SurroundingRectangle(recap, buff=0.25, color=BLUE)
        end = Text("Bonne chance pour les exercices !", font_size=34, color=GREEN).to_edge(DOWN)

        self.play(FadeIn(box), LaggedStart(*[Write(line) for line in recap], lag_ratio=0.13, run_time=3.0))
        self.play(FadeIn(end, shift=UP * 0.2))
        self.wait(1.2)
