from manim import *
import numpy as np


class VideoLimites(Scene):
    """
    Vidéo pédagogique: Limites — formules et méthodes (1BAC SM, Maroc)
    Durée visée: 6 à 10 minutes (selon rythme voix-off).
    """

    def construct(self):
        self.scene_1_intro()
        self.scene_2_intuition_graphique()
        self.scene_3_definition_simple()
        self.scene_4_proprietes_formules()
        self.scene_5_limites_usuelles()
        self.scene_6_methodes()
        self.scene_7_pieges()
        self.scene_8_mini_exercices()

    # ------------------------------------------------------------------
    # Scene 1 — Intro
    # ------------------------------------------------------------------
    def scene_1_intro(self):
        title = Text("Limites d’une fonction — 1BAC SM (Maroc)", font_size=40, weight=BOLD)
        subtitle = Text("Formules et méthodes essentielles", font_size=30, color=BLUE)

        objectifs_title = Text("Objectifs", font_size=32, color=YELLOW).to_edge(LEFT).shift(UP * 0.6)
        objectifs = VGroup(
            MathTex(r"\bullet\ \text{Comprendre la notion de limite}", font_size=34),
            MathTex(r"\bullet\ \text{Utiliser les propriétés de calcul}", font_size=34),
            MathTex(r"\bullet\ \text{Appliquer des méthodes classiques}", font_size=34),
            MathTex(r"\bullet\ \text{Éviter les pièges fréquents}", font_size=34),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        objectifs.next_to(objectifs_title, DOWN, aligned_edge=LEFT)

        self.play(Write(title))
        self.play(FadeIn(subtitle, shift=UP * 0.2))
        self.wait(0.8)
        self.play(FadeOut(subtitle), title.animate.to_edge(UP))
        self.play(FadeIn(objectifs_title, shift=RIGHT * 0.2))
        self.play(LaggedStart(*[Write(obj) for obj in objectifs], lag_ratio=0.25, run_time=2.5))
        self.wait(1.2)
        self.play(*[FadeOut(mob) for mob in [title, objectifs_title, objectifs]])

    # ------------------------------------------------------------------
    # Scene 2 — Intuition graphique
    # ------------------------------------------------------------------
    def scene_2_intuition_graphique(self):
        title = Text("Intuition graphique", font_size=36, color=YELLOW).to_edge(UP)
        axes = Axes(
            x_range=[-1, 5, 1],
            y_range=[-1, 6, 1],
            x_length=8,
            y_length=4.5,
            axis_config={"include_numbers": True, "font_size": 24},
            tips=False,
        )
        axes.to_edge(DOWN, buff=0.5)

        # Courbe simple: f(x) = x + 1
        graph = axes.plot(lambda x: x + 1, x_range=[-0.5, 4.5], color=BLUE)

        a_value = 2
        a_line = axes.get_vertical_line(axes.c2p(a_value, 0), color=GRAY)
        a_label = MathTex(r"x=a", font_size=32).next_to(a_line, DOWN)
        f_a_point = Dot(axes.c2p(a_value, a_value + 1), color=RED)
        f_a_label = MathTex(r"L", font_size=32, color=RED).next_to(f_a_point, UR, buff=0.1)

        moving_dot = Dot(color=ORANGE)
        left_text = MathTex(r"x\to a^-", font_size=32, color=ORANGE).to_corner(UL).shift(DOWN * 0.7)
        right_text = MathTex(r"x\to a^+", font_size=32, color=GREEN).next_to(left_text, DOWN, aligned_edge=LEFT)
        limit_text = MathTex(r"\lim_{x\to a} f(x)=L", font_size=40).to_corner(UR).shift(DOWN * 0.7)

        self.play(Write(title))
        self.play(Create(axes))
        self.play(Create(graph))
        self.play(Create(a_line), Write(a_label))
        self.play(FadeIn(f_a_point), Write(f_a_label))

        # Approche à gauche
        self.play(Write(left_text))
        for x in np.linspace(0.2, a_value - 0.08, 18):
            moving_dot.move_to(axes.c2p(float(x), float(x + 1)))
            self.add(moving_dot)
            self.wait(0.03)

        # Approche à droite
        self.play(Write(right_text))
        moving_dot.set_color(GREEN)
        for x in np.linspace(4.2, a_value + 0.08, 18):
            moving_dot.move_to(axes.c2p(float(x), float(x + 1)))
            self.add(moving_dot)
            self.wait(0.03)

        self.play(Write(limit_text))
        self.wait(1.2)
        self.play(
            *[FadeOut(mob) for mob in [
                title, axes, graph, a_line, a_label, f_a_point, f_a_label,
                moving_dot, left_text, right_text, limit_text
            ]]
        )

    # ------------------------------------------------------------------
    # Scene 3 — Définition niveau bac
    # ------------------------------------------------------------------
    def scene_3_definition_simple(self):
        title = Text("Définition (niveau bac)", font_size=36, color=YELLOW).to_edge(UP)
        definition = MathTex(r"\lim_{x\to a} f(x)=L", font_size=62)
        phrase = MathTex(
            r"x\ \text{proche de}\ a\ \Rightarrow\ f(x)\ \text{proche de}\ L",
            font_size=42,
        ).next_to(definition, DOWN, buff=0.6)

        example_title = Text("Exemple", font_size=30, color=BLUE).next_to(phrase, DOWN, buff=0.8)
        ex_formula = MathTex(r"f(x)=2x,\quad x\to 1\quad\Rightarrow\quad \lim_{x\to1}2x=2", font_size=44)
        ex_formula.next_to(example_title, DOWN, buff=0.3)

        self.play(Write(title))
        self.play(Write(definition))
        self.play(FadeIn(phrase, shift=UP * 0.2))
        self.play(Write(example_title), Write(ex_formula))
        self.wait(1.4)
        self.play(FadeOut(title), FadeOut(definition), FadeOut(phrase), FadeOut(example_title), FadeOut(ex_formula))

    # ------------------------------------------------------------------
    # Scene 4 — Propriétés / formules de calcul
    # ------------------------------------------------------------------
    def scene_4_proprietes_formules(self):
        title = Text("Propriétés de calcul", font_size=36, color=YELLOW).to_edge(UP)
        self.play(Write(title))

        formulas = [
            (r"\lim(f+g)=\lim f+\lim g", r"\lim_{x\to2}(x+1+x^2)=3+4=7"),
            (r"\lim(f-g)=\lim f-\lim g", r"\lim_{x\to3}(x^2-x)=9-3=6"),
            (r"\lim(kf)=k\lim f", r"\lim_{x\to1}(5x)=5\cdot1=5"),
            (r"\lim(fg)=(\lim f)(\lim g)", r"\lim_{x\to2}(x(x+1))=2\cdot3=6"),
            (r"\lim\left(\frac{f}{g}\right)=\frac{\lim f}{\lim g}\ \text{si}\ \lim g\neq0", r"\lim_{x\to1}\frac{x+2}{x+1}=\frac{3}{2}"),
        ]

        rows = VGroup()
        for i, (fml, ex) in enumerate(formulas):
            left = MathTex(fml, font_size=34)
            right = MathTex(ex, font_size=30, color=BLUE_D)
            row = VGroup(left, right).arrange(RIGHT, buff=0.9)
            box = SurroundingRectangle(row, buff=0.12, color=GRAY_B, stroke_width=1.6)
            row_with_box = VGroup(box, row)
            rows.add(row_with_box)

        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.23)
        rows.scale(0.86).next_to(title, DOWN, buff=0.35)

        for row in rows:
            self.play(FadeIn(row[0]), Write(row[1][0]), FadeIn(row[1][1], shift=RIGHT * 0.2), run_time=1.0)
            self.wait(0.22)

        self.wait(1.0)
        self.play(FadeOut(rows), FadeOut(title))

    # ------------------------------------------------------------------
    # Scene 5 — Limites usuelles
    # ------------------------------------------------------------------
    def scene_5_limites_usuelles(self):
        title = Text("Limites usuelles (1BAC)", font_size=36, color=YELLOW).to_edge(UP)
        self.play(Write(title))

        usuals = VGroup(
            MathTex(r"\lim_{x\to a} c = c", font_size=42),
            MathTex(r"\lim_{x\to a} x = a", font_size=42),
            MathTex(r"\lim_{x\to a} x^n = a^n", font_size=42),
            MathTex(r"\lim_{x\to a} \frac{1}{x} = \frac{1}{a}\quad (a\neq0)", font_size=42),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        usuals.next_to(title, DOWN, buff=0.55)

        df_box = SurroundingRectangle(usuales := usuals, buff=0.28, color=BLUE)
        df_text = MathTex(r"\text{Df: vérifier les conditions}\ (\text{ex: dénominateur}\neq0)", font_size=34, color=BLUE)
        df_text.next_to(df_box, DOWN, buff=0.4)

        self.play(LaggedStart(*[Write(line) for line in usuals], lag_ratio=0.25, run_time=2.2))
        self.play(Create(df_box), Write(df_text))
        self.wait(1.2)
        self.play(FadeOut(title), FadeOut(usuales), FadeOut(df_box), FadeOut(df_text))

    # ------------------------------------------------------------------
    # Scene 6 — Méthodes
    # ------------------------------------------------------------------
    def scene_6_methodes(self):
        title = Text("Méthodes de calcul", font_size=36, color=YELLOW).to_edge(UP)
        self.play(Write(title))

        method_1 = VGroup(
            Text("1) Substitution directe", font_size=30, color=BLUE),
            MathTex(r"\lim_{x\to2}(x^2+1)=2^2+1=5", font_size=38),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(LEFT).shift(UP * 1.4)

        method_2 = VGroup(
            Text("2) Factorisation / simplification (forme 0/0)", font_size=30, color=BLUE),
            MathTex(r"\lim_{x\to1}\frac{x^2-1}{x-1}=\lim_{x\to1}\frac{(x-1)(x+1)}{x-1}=\lim_{x\to1}(x+1)=2", font_size=33),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(method_1, DOWN, aligned_edge=LEFT, buff=0.55)

        method_3 = VGroup(
            Text("3) Rationalisation (racines)", font_size=30, color=BLUE),
            MathTex(r"\lim_{x\to0}\frac{\sqrt{x+4}-2}{x}", font_size=34),
            MathTex(r"=\lim_{x\to0}\frac{(\sqrt{x+4}-2)(\sqrt{x+4}+2)}{x(\sqrt{x+4}+2)}", font_size=30),
            MathTex(r"=\lim_{x\to0}\frac{x}{x(\sqrt{x+4}+2)}=\lim_{x\to0}\frac{1}{\sqrt{x+4}+2}=\frac14", font_size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(method_2, DOWN, aligned_edge=LEFT, buff=0.45)
        method_3.scale(0.95)

        self.play(FadeIn(method_1, shift=RIGHT * 0.2))
        self.wait(0.7)
        self.play(FadeIn(method_2, shift=RIGHT * 0.2))
        self.wait(0.8)

        # Nettoyage partiel pour garder de la place
        self.play(FadeOut(method_1), method_2.animate.to_edge(UP).shift(DOWN * 0.8))
        self.play(FadeIn(method_3, shift=UP * 0.2))
        self.wait(1.0)

        # Limites à l'infini: degrés
        self.play(FadeOut(method_2), FadeOut(method_3))
        inf_title = Text("4) Limites en +∞ / −∞ (comparer les degrés)", font_size=30, color=BLUE)
        inf_title.next_to(title, DOWN, buff=0.55)

        inf_rules = VGroup(
            MathTex(r"\deg(P)<\deg(Q)\ \Rightarrow\ \lim\frac{P(x)}{Q(x)}=0", font_size=34),
            MathTex(r"\deg(P)=\deg(Q)\ \Rightarrow\ \lim\frac{P(x)}{Q(x)}=\frac{\text{coef dominant de }P}{\text{coef dominant de }Q}", font_size=31),
            MathTex(r"\deg(P)>\deg(Q)\ \Rightarrow\ \text{la limite est de type }\pm\infty\ \text{(selon les signes)}", font_size=31),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).next_to(inf_title, DOWN, buff=0.45)

        ex_inf = VGroup(
            MathTex(r"\lim_{x\to+\infty}\frac{3x^2+1}{x^2-5x}=\frac{3}{1}=3", font_size=35, color=GREEN_D),
            MathTex(r"\lim_{x\to-\infty}\frac{2x^3-x}{x^2+1}=-\infty", font_size=35, color=GREEN_D),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(inf_rules, DOWN, buff=0.5)

        self.play(Write(inf_title))
        self.play(LaggedStart(*[Write(r) for r in inf_rules], lag_ratio=0.22, run_time=2.2))
        self.play(FadeIn(ex_inf, shift=UP * 0.2))
        self.wait(1.4)

        self.play(FadeOut(title), FadeOut(inf_title), FadeOut(inf_rules), FadeOut(ex_inf))

    # ------------------------------------------------------------------
    # Scene 7 — Pièges fréquents
    # ------------------------------------------------------------------
    def scene_7_pieges(self):
        title = Text("Pièges fréquents", font_size=36, color=YELLOW).to_edge(UP)

        flash_items = VGroup(
            MathTex(r"\text{Piège 1: division par }0", font_size=46, color=RED),
            MathTex(r"\text{Piège 2: confondre limite et valeur }f(a)", font_size=46, color=ORANGE),
            MathTex(r"\text{Piège 3: oublier }\lim g\neq0\ \text{dans }\frac{f}{g}", font_size=42, color=RED_D),
        ).arrange(DOWN, buff=0.5)

        self.play(Write(title))
        for item in flash_items:
            self.play(FadeIn(item, scale=1.05), run_time=0.7)
            self.wait(0.4)
        self.wait(0.7)
        self.play(FadeOut(title), FadeOut(flash_items))

    # ------------------------------------------------------------------
    # Scene 8 — Mini-exercices finaux
    # ------------------------------------------------------------------
    def scene_8_mini_exercices(self):
        title = Text("Mini-exercices", font_size=36, color=YELLOW).to_edge(UP)
        ex1 = MathTex(r"\text{Ex1: }\lim_{x\to2}\frac{x^2-4}{x-2}\ \ ?", font_size=44)
        ex2 = MathTex(r"\text{Ex2: }\lim_{x\to+\infty}\frac{3x^2+1}{x^2-5x}\ \ ?", font_size=44)
        ex_group = VGroup(ex1, ex2).arrange(DOWN, aligned_edge=LEFT, buff=0.5).next_to(title, DOWN, buff=0.8)

        pause_msg = Text("Pause 3 secondes...", font_size=30, color=BLUE).next_to(ex_group, DOWN, buff=0.8)

        self.play(Write(title), FadeIn(ex_group, shift=UP * 0.2))
        self.play(FadeIn(pause_msg))
        self.wait(3)

        corr_title = Text("Correction", font_size=32, color=GREEN).next_to(ex_group, DOWN, buff=0.8)
        corr1 = MathTex(
            r"\lim_{x\to2}\frac{x^2-4}{x-2}=\lim_{x\to2}\frac{(x-2)(x+2)}{x-2}=\lim_{x\to2}(x+2)=4",
            font_size=32,
            color=GREEN_D,
        )
        corr2 = MathTex(
            r"\lim_{x\to+\infty}\frac{3x^2+1}{x^2-5x}=\frac{3}{1}=3",
            font_size=36,
            color=GREEN_D,
        )
        corr_group = VGroup(corr1, corr2).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(corr_title, DOWN, buff=0.25)

        self.play(FadeOut(pause_msg))
        self.play(Write(corr_title))
        self.play(LaggedStart(Write(corr1), Write(corr2), lag_ratio=0.4, run_time=2.6))
        self.wait(1.5)

        outro = Text("Bravo ! Révisez les méthodes et les conditions de Df.", font_size=30, color=YELLOW)
        outro.to_edge(DOWN)
        self.play(FadeIn(outro, shift=UP * 0.2))
        self.wait(1.8)
