from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.label import MDLabel
from kivymd.uix.screenmanager import MDScreenManager
from kivy.core.window import Window
from kivymd.uix.dialog import MDDialog, MDDialogHeadlineText, MDDialogButtonContainer
from kivy.uix.widget import Widget

import numpy as np
import pandas as pd
import math
import csv
import random

from user.user import OrderManager


class MainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Aqua"
        self.prods = pd.read_csv("data/products.csv", delimiter=',')
        with open("data/sections.txt", encoding="utf-8") as f:
            self.sections = f.read().split("\n")
        self.cart = [0 for _ in range(len(self.prods))]

        self.om = OrderManager("localhost", 11111)
        self.sm = MDScreenManager()
        self.auth_screen = Builder.load_file("data/kv/auth.kv")
        self.cart_screen = Builder.load_file("data/kv/cart.kv")
        self.choose_screen = Builder.load_file("data/kv/choosing.kv")

        # section buttons
        for i, sect in enumerate(self.sections):
            btn = MDButton(
                MDButtonText(text=sect),
                on_release=self.build_choose_screen,
                pos_hint={"center_y": 0.5}
            )
            btn.section_id = i
            self.choose_screen.ids.sections.add_widget(btn)

        self.sm.add_widget(self.choose_screen)
        self.sm.add_widget(self.auth_screen)
        self.sm.add_widget(self.cart_screen)
        # self.sm.add_widget(cart_screen)
        wgt = Widget()
        wgt.section_id = 0
        self.build_choose_screen(wgt)
        del wgt

        return self.sm

    def build_choose_screen(self, instance):
        # products
        sect = self.prods[self.prods.section_id == instance.section_id]
        self.choose_screen.ids.btns.clear_widgets()
        for i, row in sect.iterrows():
            ctx = {"img": "data/images/product" + str(i) + ".png", "name": f"[b]{row["product_name"]}[/b]",
                   "price": f"[b]{row["product_cost"]}₽[/b]", "id": i}

            btn = Builder.template("ProductButton", **ctx)
            btn.ids.btn.bind(on_release=self.change_cart)
            self.choose_screen.ids.btns.add_widget(btn)

        self.choose_screen.ids.btns.height = str(math.ceil(len(sect) / 2) * 310) + "dp"
        self.update_choose()


    def login_btn(self):
        # something with server
        if self.auth_screen.ids.username_textfield.text == "user" and self.auth_screen.ids.password_textfield.text == "password":
            self.sm.current = "choose"

        else:
            print(self.auth_screen.ids.username_textfield.text)

            dlg = MDDialog(
                MDDialogHeadlineText(text="Неверное имя пользователя или пароль"))
            dlg.add_widget(
                MDDialogButtonContainer(
                    MDButton(
                        MDButtonText(text="Ладно"),
                        on_release=dlg.dismiss
                    )
                )
            )
            dlg.open()


    def change_cart(self, instance):
        add = not instance.parent.parent.added
        instance.parent.parent.added = add
        self.cart[instance.parent.parent.prod_id] = int(add)
        instance.parent.parent.ids.btn_text.text = "Убрать из корзины" if add else "Добавить в корзину"
        self.upd_cart_sum()
        print(self.cart)


    def update_cart(self):
        self.cart_screen.ids.container.clear_widgets()
        for i, row in self.prods.iterrows():
            if self.cart[i] > 0:
                ctx = {"img": "data/images/product" + str(i) + ".png", "name": f"[b]{row["product_name"]}[/b]",
                       "price": f"[b]{row["product_cost"]}₽[/b]", "id": i}

                item = Builder.template("CartItem", **ctx)
                item.ids.plus.bind(on_release=self.some_cart_btn)
                item.ids.minus.bind(on_release=self.some_cart_btn)
                item.ids.lbl.text = str(self.cart[i])

                self.cart_screen.ids.container.height += item.height
                self.cart_screen.ids.container.add_widget(item)

        self.cart_screen.ids.container.add_widget(Widget())
        self.sm.current = "cart"
        self.upd_cart_sum()


    def update_choose(self):
        for i, widget in enumerate(self.choose_screen.ids.btns.children):
            if self.cart[widget.prod_id] == 0:
                widget.added = False
                widget.ids.btn_text.text = "Добавить в корзину"
            else:
                widget.added = True
                widget.ids.btn_text.text = "Убрать из корзины"
        self.sm.current = "choose"


    def some_cart_btn(self, instance):
        root = instance.parent.parent.parent
        if instance.plus and self.cart[root.prod_id] < 99:
            self.cart[root.prod_id] += 1
        if not instance.plus and self.cart[root.prod_id] > 0:
            self.cart[root.prod_id] -= 1

        root.ids.lbl.text = str(self.cart[root.prod_id])
        self.upd_cart_sum()
# clash royale

    def upd_cart_sum(self):
        res = 0
        for count, cost in zip(self.cart, self.prods["product_cost"]):
            res += count * cost

        self.cart_screen.ids.sum_lbl.text = f"[b]{res}₽[/b]"


    def order(self):
        if sum(self.cart) > 0:
            ord_id = random.randrange(10000)

            dlg = MDDialog(
                MDDialogHeadlineText(text="Номер вашего заказа "+str(ord_id)))
            dlg.add_widget(
                MDDialogButtonContainer(
                    MDButton(
                        MDButtonText(text="Ладно"),
                        on_release=dlg.dismiss
                    )
                )
            )
            dlg.open()

            self.om.SendOrder(ord_id, 0, 0, self.cart)
            self.cart = [0 for _ in range(len(self.prods))]
        self.update_choose()

if __name__ == "__main__":
    Window.size = (600, 1000)
    MainApp().run()

