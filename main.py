import flet as ft

from database import *


# =========================================================
# THEME
# =========================================================

BG = "#050914"
SURFACE = "#0A1120"
CARD = "#0D1728"
CARD_HOVER = "#122039"

TEXT = "#F1F5F9"
MUTED = "#7D8CA5"
MUTED_2 = "#53627A"

BLUE = "#6D8CFF"
BLUE_DARK = "#17254B"

GREEN = "#43D6A0"
GREEN_DARK = "#103A35"

ORANGE = "#FF9B4A"
ORANGE_DARK = "#4A2D18"

RED = "#FF6B7A"
RED_DARK = "#421C25"

BORDER = "#17243A"


# =========================================================
# MAIN
# =========================================================

def main(page: ft.Page):

    page.title = "وسایل خونه"
    page.bgcolor = BG
    page.padding = 0
    page.rtl = True

    create_tables()

    # =====================================================
    # HELPERS
    # =====================================================

    def clear_page():
        page.clean()
        page.update()

    def title_text(text, size=26):
        return ft.Text(
            text,
            size=size,
            weight=ft.FontWeight.BOLD,
            color=TEXT,
        )

    def subtitle_text(text):
        return ft.Text(
            text,
            size=13,
            color=MUTED,
        )

    def make_button(
        text,
        on_click,
        bgcolor=CARD,
        color=TEXT,
        width=None,
    ):
        return ft.Container(
            content=ft.Text(
                text,
                color=color,
                size=13,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER,
            ),
            bgcolor=bgcolor,
            border_radius=12,
            padding=ft.Padding(16, 11, 16, 11),
            width=width,
            on_click=on_click,
        )

    def make_back_button(on_click):
        return ft.Container(
            content=ft.Text(
                "→  بازگشت",
                color=MUTED,
                size=13,
                weight=ft.FontWeight.BOLD,
            ),
            padding=ft.Padding(14, 10, 14, 10),
            bgcolor=CARD,
            border_radius=12,
            on_click=on_click,
        )

    def make_page_header(
        title,
        subtitle="",
        on_back=None,
    ):
        controls = []

        if on_back:
            controls.append(
                make_back_button(on_back)
            )

        controls.append(
            ft.Container(
                expand=True,
                content=ft.Column(
                    controls=[
                        ft.Text(
                            title,
                            size=25,
                            weight=ft.FontWeight.BOLD,
                            color=TEXT,
                        ),
                        ft.Text(
                            subtitle,
                            size=12,
                            color=MUTED,
                        ) if subtitle else ft.Container(),
                    ],
                    spacing=4,
                ),
            )
        )

        return ft.Container(
            padding=ft.Padding(20, 22, 20, 10),
            content=ft.Row(
                controls=controls,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )

    def make_section_label(text):
        return ft.Row(
            controls=[
                ft.Container(
                    width=5,
                    height=22,
                    bgcolor=GREEN,
                    border_radius=10,
                ),
                ft.Text(
                    text,
                    color=TEXT,
                    size=16,
                    weight=ft.FontWeight.BOLD,
                ),
            ],
            spacing=9,
        )

    # =====================================================
    # ITEM DETAILS
    # =====================================================

    def show_item_details(item):

        item_id, name, location, description = item

        clear_page()

        def delete_item_confirm():

            def confirm_delete(e):

                delete_item(item_id)

                dialog.open = False
                page.update()

                show_search()

            def cancel_delete(e):

                dialog.open = False
                page.update()

            dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text(
                    "حذف وسیله",
                    color=TEXT,
                ),
                content=ft.Text(
                    f'مطمئنی می‌خوای «{name}» رو حذف کنی؟',
                    color=MUTED,
                ),
                actions=[
                    ft.TextButton(
                        "انصراف",
                        on_click=cancel_delete,
                    ),
                    ft.TextButton(
                        "حذف",
                        on_click=confirm_delete,
                    ),
                ],
            )

            page.overlay.append(dialog)
            dialog.open = True
            page.update()

        details = ft.Column(
            controls=[
                make_section_label("اطلاعات وسیله"),

                ft.Container(
                    bgcolor=CARD,
                    border_radius=18,
                    padding=20,
                    content=ft.Column(
                        controls=[

                            ft.Text(
                                name,
                                size=23,
                                weight=ft.FontWeight.BOLD,
                                color=TEXT,
                            ),

                            ft.Container(
                                height=1,
                                bgcolor=BORDER,
                            ),

                            ft.Text(
                                "مکان",
                                size=11,
                                color=MUTED,
                            ),

                            ft.Text(
                                location if location else "مکانی ثبت نشده",
                                size=14,
                                color=TEXT if location else MUTED_2,
                            ),

                            ft.Container(height=5),

                            ft.Text(
                                "توضیحات",
                                size=11,
                                color=MUTED,
                            ),

                            ft.Text(
                                description if description else "توضیحی ثبت نشده",
                                size=14,
                                color=TEXT if description else MUTED_2,
                            ),
                        ],
                        spacing=9,
                    ),
                ),

                ft.Row(
                    controls=[
                        make_button(
                            "✎  ویرایش",
                            lambda e: show_edit_item(item),
                            bgcolor=BLUE_DARK,
                            color=BLUE,
                        ),

                        make_button(
                            "حذف",
                            lambda e: delete_item_confirm(),
                            bgcolor=RED_DARK,
                            color=RED,
                        ),
                    ],
                    spacing=10,
                    wrap=True,
                ),
            ],
            spacing=16,
        )

        page.add(
            ft.Column(
                controls=[
                    make_page_header(
                        "جزئیات وسیله",
                        "اطلاعات کامل وسیله ثبت‌شده",
                        show_search,
                    ),
                    ft.Container(
                        content=details,
                        padding=ft.Padding(20, 10, 20, 30),
                    ),
                ],
                expand=True,
                scroll=ft.ScrollMode.AUTO,
            )
        )

        page.update()

    # =====================================================
    # EDIT HOUSEHOLD ITEM
    # =====================================================

    def show_edit_item(item):

        item_id, old_name, old_location, old_description = item

        clear_page()

        name_field = ft.TextField(
            label="نام وسیله",
            value=old_name,
            autofocus=True,
            rtl=True,
            text_align=ft.TextAlign.RIGHT,
        )

        location_field = ft.TextField(
            label="مکان",
            value=old_location or "",
            rtl=True,
            text_align=ft.TextAlign.RIGHT,
        )

        description_field = ft.TextField(
            label="توضیحات",
            value=old_description or "",
            multiline=True,
            min_lines=3,
            max_lines=5,
            rtl=True,
            text_align=ft.TextAlign.RIGHT,
        )

        def save_changes(e):

            name = name_field.value.strip()

            if not name:
                name_field.error_text = "نام وسیله را وارد کن."
                page.update()
                return

            update_item(
                item_id,
                name,
                location_field.value.strip(),
                description_field.value.strip(),
            )

            updated_item = (
                item_id,
                name,
                location_field.value.strip(),
                description_field.value.strip(),
            )

            show_item_details(updated_item)

        form = ft.Column(
            controls=[
                make_section_label("ویرایش اطلاعات"),

                ft.Container(
                    bgcolor=CARD,
                    border_radius=18,
                    padding=20,
                    content=ft.Column(
                        controls=[
                            name_field,
                            location_field,
                            description_field,
                        ],
                        spacing=15,
                    ),
                ),

                make_button(
                    "✓  ذخیره تغییرات",
                    save_changes,
                    bgcolor=GREEN_DARK,
                    color=GREEN,
                ),
            ],
            spacing=16,
        )

        page.add(
            ft.Column(
                controls=[
                    make_page_header(
                        "ویرایش وسیله",
                        "اطلاعات وسیله را تغییر بده",
                        lambda e: show_item_details(item),
                    ),
                    ft.Container(
                        content=form,
                        padding=ft.Padding(20, 10, 20, 30),
                    ),
                ],
                expand=True,
                scroll=ft.ScrollMode.AUTO,
            )
        )

        page.update()

    # =====================================================
    # SEARCH
    # =====================================================

    def show_search():

        clear_page()

        results_column = ft.Column(
            spacing=10,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
        )

        search_field = ft.TextField(
            hint_text="مثلاً تلویزیون، جارو، کابل...",
            rtl=True,
            text_align=ft.TextAlign.RIGHT,
        )

        def refresh_results():

            results_column.controls.clear()

            items = search_items(
                search_field.value or ""
            )

            if not items:

                results_column.controls.append(
                    ft.Container(
                        bgcolor=CARD,
                        border_radius=18,
                        padding=25,
                        content=ft.Column(
                            controls=[
                                ft.Text(
                                    "⌕",
                                    size=35,
                                    color=MUTED_2,
                                    text_align=ft.TextAlign.CENTER,
                                ),
                                ft.Text(
                                    "چیزی پیدا نشد",
                                    size=16,
                                    weight=ft.FontWeight.BOLD,
                                    color=TEXT,
                                    text_align=ft.TextAlign.CENTER,
                                ),
                                ft.Text(
                                    "عبارت دیگری را امتحان کن.",
                                    size=12,
                                    color=MUTED,
                                    text_align=ft.TextAlign.CENTER,
                                ),
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=7,
                        ),
                    )
                )

            else:

                for item in items:

                    item_id, name, location, description = item

                    def open_item(
                        e,
                        current_item=item,
                    ):
                        show_item_details(current_item)

                    results_column.controls.append(
                        ft.Container(
                            bgcolor=CARD,
                            border_radius=16,
                            padding=16,
                            on_click=open_item,
                            on_hover=lambda e: None,
                            content=ft.Row(
                                controls=[
                                    ft.Container(
                                        width=42,
                                        height=42,
                                        bgcolor=BLUE_DARK,
                                        border_radius=12,
                                        alignment=ft.Alignment.CENTER,
                                        content=ft.Text(
                                            "⌂",
                                            color=BLUE,
                                            size=19,
                                        ),
                                    ),

                                    ft.Column(
                                        controls=[
                                            ft.Text(
                                                name,
                                                color=TEXT,
                                                size=15,
                                                weight=ft.FontWeight.BOLD,
                                            ),
                                            ft.Text(
                                                location
                                                if location
                                                else "مکان ثبت نشده",
                                                color=MUTED,
                                                size=11,
                                            ),
                                        ],
                                        spacing=4,
                                        expand=True,
                                    ),

                                    ft.Text(
                                        "←",
                                        color=MUTED,
                                        size=18,
                                    ),
                                ],
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                        )
                    )

            page.update()

        search_field.on_change = lambda e: refresh_results()

        page.add(
            ft.Column(
                controls=[
                    make_page_header(
                        "جست‌وجوی وسایل",
                        "هر چیزی که قبلاً ثبت کردی اینجاست",
                        show_home,
                    ),

                    ft.Container(
                        padding=ft.Padding(20, 5, 20, 12),
                        content=search_field,
                    ),

                    ft.Container(
                        padding=ft.Padding(20, 0, 20, 30),
                        content=results_column,
                        expand=True,
                    ),
                ],
                expand=True,
            )
        )

        refresh_results()

    # =====================================================
    # ADD HOUSEHOLD ITEM
    # =====================================================

    def show_add_item():

        clear_page()

        name_field = ft.TextField(
            label="نام وسیله *",
            hint_text="مثلاً تلویزیون",
            autofocus=True,
            rtl=True,
            text_align=ft.TextAlign.RIGHT,
        )

        location_field = ft.TextField(
            label="مکان",
            hint_text="مثلاً اتاق خواب",
            rtl=True,
            text_align=ft.TextAlign.RIGHT,
        )

        description_field = ft.TextField(
            label="توضیحات",
            hint_text="هر چیزی که لازم است درباره این وسیله بدانی...",
            multiline=True,
            min_lines=4,
            max_lines=6,
            rtl=True,
            text_align=ft.TextAlign.RIGHT,
        )

        def save_item(e):

            name = name_field.value.strip()

            if not name:

                name_field.error_text = "نام وسیله را وارد کن."
                page.update()

                return

            add_item(
                name,
                location_field.value.strip(),
                description_field.value.strip(),
            )

            show_home()

        form = ft.Column(
            controls=[
                make_section_label("وسیله جدید"),

                ft.Container(
                    bgcolor=CARD,
                    border_radius=18,
                    padding=20,
                    content=ft.Column(
                        controls=[
                            name_field,
                            location_field,
                            description_field,
                        ],
                        spacing=15,
                    ),
                ),

                make_button(
                    "＋  ثبت وسیله",
                    save_item,
                    bgcolor=GREEN_DARK,
                    color=GREEN,
                ),
            ],
            spacing=16,
        )

        page.add(
            ft.Column(
                controls=[
                    make_page_header(
                        "اضافه کردن وسیله",
                        "یک وسیله جدید به خانه اضافه کن",
                        show_home,
                    ),

                    ft.Container(
                        content=form,
                        padding=ft.Padding(20, 10, 20, 30),
                    ),
                ],
                expand=True,
                scroll=ft.ScrollMode.AUTO,
            )
        )

        page.update()

    # =====================================================
    # ADD REMINDER LIST
    # =====================================================

    def show_add_reminder_list():

        clear_page()

        reminder_items = []

        list_name_field = ft.TextField(
            label="نام لیست *",
            hint_text="مثلاً فوتبال، سفر، سالن...",
            autofocus=True,
            rtl=True,
            text_align=ft.TextAlign.RIGHT,
        )

        item_name_field = ft.TextField(
            label="نام وسیله",
            hint_text="مثلاً کفش",
            rtl=True,
            text_align=ft.TextAlign.RIGHT,
        )

        items_column = ft.Column(
            spacing=8,
        )

        def refresh_items():

            items_column.controls.clear()

            if not reminder_items:

                items_column.controls.append(
                    ft.Text(
                        "هنوز وسیله‌ای اضافه نشده.",
                        color=MUTED,
                        size=12,
                    )
                )

            else:

                for index, item_name in enumerate(
                    reminder_items,
                    start=1,
                ):

                    items_column.controls.append(
                        ft.Container(
                            bgcolor=SURFACE,
                            border_radius=12,
                            padding=12,
                            content=ft.Row(
                                controls=[
                                    ft.Text(
                                        str(index),
                                        color=GREEN,
                                        size=12,
                                        width=25,
                                        text_align=ft.TextAlign.CENTER,
                                    ),

                                    ft.Text(
                                        item_name,
                                        color=TEXT,
                                        size=13,
                                        expand=True,
                                    ),
                                ],
                            ),
                        )
                    )

            page.update()

        def add_reminder_item(e):

            name = item_name_field.value.strip()

            if not name:

                item_name_field.error_text = (
                    "نام وسیله را وارد کن."
                )

                page.update()

                return

            reminder_items.append(name)

            item_name_field.value = ""

            refresh_items()

        def save_list(e):

            list_name = list_name_field.value.strip()

            if not list_name:

                list_name_field.error_text = (
                    "نام لیست را وارد کن."
                )

                page.update()

                return

            if not reminder_items:

                item_name_field.error_text = (
                    "حداقل یک وسیله اضافه کن."
                )

                page.update()

                return

            list_id = create_list(list_name)

            for position, item_name in enumerate(
                reminder_items,
                start=1,
            ):

                add_list_item(
                    list_id,
                    item_name,
                    position,
                )

            show_reminder_lists()

        page.add(
            ft.Column(
                controls=[
                    make_page_header(
                        "ساخت لیست جدید",
                        "برای سفر، فوتبال، سالن و هر کاری که وسایل مخصوص خودش را دارد",
                        show_home,
                    ),

                    ft.Container(
                        padding=ft.Padding(20, 5, 20, 30),
                        content=ft.Column(
                            controls=[

                                make_section_label(
                                    "نام لیست"
                                ),

                                ft.Container(
                                    bgcolor=CARD,
                                    border_radius=18,
                                    padding=18,
                                    content=list_name_field,
                                ),

                                make_section_label(
                                    "وسایل لیست"
                                ),

                                ft.Container(
                                    bgcolor=CARD,
                                    border_radius=18,
                                    padding=18,
                                    content=ft.Column(
                                        controls=[
                                            item_name_field,

                                            make_button(
                                                "＋  افزودن وسیله به لیست",
                                                add_reminder_item,
                                                bgcolor=BLUE_DARK,
                                                color=BLUE,
                                            ),

                                            ft.Container(
                                                height=5
                                            ),

                                            items_column,
                                        ],
                                        spacing=12,
                                    ),
                                ),

                                make_button(
                                    "✓  ذخیره لیست",
                                    save_list,
                                    bgcolor=GREEN_DARK,
                                    color=GREEN,
                                ),
                            ],
                            spacing=15,
                        ),
                    ),
                ],
                expand=True,
                scroll=ft.ScrollMode.AUTO,
            )
        )

        refresh_items()

    # =====================================================
    # REMINDER LISTS
    # =====================================================

    def show_reminder_lists():

        clear_page()

        lists_column = ft.Column(
            spacing=10,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
        )

        search_field = ft.TextField(
            hint_text="جست‌وجوی لیست...",
            rtl=True,
            text_align=ft.TextAlign.RIGHT,
        )

        def show_list_items(reminder_list):

            list_id, list_name = reminder_list

            clear_page()

            items_column = ft.Column(
                spacing=10,
                expand=True,
                scroll=ft.ScrollMode.AUTO,
            )

            def refresh_items():

                items_column.controls.clear()

                items = get_list_items(list_id)

                if not items:

                    items_column.controls.append(
                        ft.Container(
                            bgcolor=CARD,
                            border_radius=18,
                            padding=25,
                            content=ft.Column(
                                controls=[
                                    ft.Text(
                                        "☷",
                                        size=34,
                                        color=MUTED_2,
                                    ),
                                    ft.Text(
                                        "این لیست خالی است",
                                        size=15,
                                        color=TEXT,
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                    ft.Text(
                                        "از دکمه افزودن وسیله استفاده کن.",
                                        size=12,
                                        color=MUTED,
                                    ),
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=7,
                            ),
                        )
                    )

                else:

                    for index, item in enumerate(
                        items,
                        start=1,
                    ):

                        item_id, item_name, position = item

                        def edit_item_click(
                            e,
                            current_item_id=item_id,
                            current_name=item_name,
                        ):

                            name_field = ft.TextField(
                                label="نام وسیله",
                                value=current_name,
                                autofocus=True,
                                rtl=True,
                                text_align=ft.TextAlign.RIGHT,
                            )

                            def save_edit(e):

                                new_name = (
                                    name_field.value.strip()
                                )

                                if not new_name:

                                    name_field.error_text = (
                                        "نام وسیله را وارد کن."
                                    )

                                    page.update()

                                    return

                                update_list_item(
                                    current_item_id,
                                    new_name,
                                )

                                dialog.open = False

                                page.update()

                                refresh_items()

                            def close_dialog(e):

                                dialog.open = False
                                page.update()

                            dialog = ft.AlertDialog(
                                modal=True,
                                title=ft.Text(
                                    "ویرایش وسیله",
                                    color=TEXT,
                                ),
                                content=ft.Container(
                                    content=name_field,
                                    width=350,
                                ),
                                actions=[
                                    ft.TextButton(
                                        "انصراف",
                                        on_click=close_dialog,
                                    ),
                                    ft.TextButton(
                                        "ذخیره",
                                        on_click=save_edit,
                                    ),
                                ],
                            )

                            page.overlay.append(dialog)
                            dialog.open = True
                            page.update()

                        def delete_item_click(
                            e,
                            current_item_id=item_id,
                            current_name=item_name,
                        ):

                            def confirm_delete(e):

                                delete_list_item(
                                    current_item_id
                                )

                                confirm_dialog.open = False

                                page.update()

                                refresh_items()

                            def cancel_delete(e):

                                confirm_dialog.open = False
                                page.update()

                            confirm_dialog = ft.AlertDialog(
                                modal=True,
                                title=ft.Text(
                                    "حذف وسیله",
                                    color=TEXT,
                                ),
                                content=ft.Text(
                                    f'مطمئنی می‌خوای «{current_name}» رو حذف کنی؟',
                                    color=MUTED,
                                ),
                                actions=[
                                    ft.TextButton(
                                        "انصراف",
                                        on_click=cancel_delete,
                                    ),
                                    ft.TextButton(
                                        "حذف",
                                        on_click=confirm_delete,
                                    ),
                                ],
                            )

                            page.overlay.append(
                                confirm_dialog
                            )

                            confirm_dialog.open = True
                            page.update()

                        items_column.controls.append(
                            ft.Container(
                                bgcolor=CARD,
                                border_radius=16,
                                padding=14,
                                content=ft.Row(
                                    controls=[

                                        ft.Container(
                                            width=34,
                                            height=34,
                                            bgcolor=GREEN_DARK,
                                            border_radius=10,
                                            alignment=ft.Alignment.CENTER,
                                            content=ft.Text(
                                                str(index),
                                                color=GREEN,
                                                size=12,
                                                weight=ft.FontWeight.BOLD,
                                            ),
                                        ),

                                        ft.Text(
                                            item_name,
                                            color=TEXT,
                                            size=14,
                                            expand=True,
                                        ),

                                        ft.TextButton(
                                            "ویرایش",
                                            on_click=edit_item_click,
                                        ),

                                        ft.TextButton(
                                            "حذف",
                                            on_click=delete_item_click,
                                        ),
                                    ],
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                            )
                        )

                page.update()

            def add_item_click(e):

                name_field = ft.TextField(
                    label="نام وسیله",
                    autofocus=True,
                    rtl=True,
                    text_align=ft.TextAlign.RIGHT,
                )

                def save_item(e):

                    name = name_field.value.strip()

                    if not name:

                        name_field.error_text = (
                            "نام وسیله را وارد کن."
                        )

                        page.update()

                        return

                    items = get_list_items(list_id)

                    next_position = len(items) + 1

                    add_list_item(
                        list_id,
                        name,
                        next_position,
                    )

                    dialog.open = False

                    page.update()

                    refresh_items()

                def close_dialog(e):

                    dialog.open = False
                    page.update()

                dialog = ft.AlertDialog(
                    modal=True,
                    title=ft.Text(
                        "افزودن وسیله",
                        color=TEXT,
                    ),
                    content=ft.Container(
                        content=name_field,
                        width=350,
                    ),
                    actions=[
                        ft.TextButton(
                            "انصراف",
                            on_click=close_dialog,
                        ),
                        ft.TextButton(
                            "افزودن",
                            on_click=save_item,
                        ),
                    ],
                )

                page.overlay.append(dialog)
                dialog.open = True
                page.update()

            def rename_list_click(e):

                name_field = ft.TextField(
                    label="نام جدید لیست",
                    value=list_name,
                    autofocus=True,
                    rtl=True,
                    text_align=ft.TextAlign.RIGHT,
                )

                def save_name(e):

                    new_name = name_field.value.strip()

                    if not new_name:

                        name_field.error_text = (
                            "نام لیست را وارد کن."
                        )

                        page.update()

                        return

                    rename_list(
                        list_id,
                        new_name,
                    )

                    dialog.open = False

                    page.update()

                    show_list_items(
                        (list_id, new_name)
                    )

                def close_dialog(e):

                    dialog.open = False
                    page.update()

                dialog = ft.AlertDialog(
                    modal=True,
                    title=ft.Text(
                        "تغییر نام لیست",
                        color=TEXT,
                    ),
                    content=ft.Container(
                        content=name_field,
                        width=350,
                    ),
                    actions=[
                        ft.TextButton(
                            "انصراف",
                            on_click=close_dialog,
                        ),
                        ft.TextButton(
                            "ذخیره",
                            on_click=save_name,
                        ),
                    ],
                )

                page.overlay.append(dialog)
                dialog.open = True
                page.update()

            def delete_list_click(e):

                def confirm_delete(e):

                    delete_list(list_id)

                    dialog.open = False

                    page.update()

                    show_reminder_lists()

                def cancel_delete(e):

                    dialog.open = False
                    page.update()

                dialog = ft.AlertDialog(
                    modal=True,
                    title=ft.Text(
                        "حذف لیست",
                        color=TEXT,
                    ),
                    content=ft.Text(
                        f'مطمئنی می‌خوای لیست «{list_name}» رو حذف کنی؟',
                        color=MUTED,
                    ),
                    actions=[
                        ft.TextButton(
                            "انصراف",
                            on_click=cancel_delete,
                        ),
                        ft.TextButton(
                            "حذف",
                            on_click=confirm_delete,
                        ),
                    ],
                )

                page.overlay.append(dialog)
                dialog.open = True
                page.update()

            page.add(
                ft.Column(
                    controls=[

                        make_page_header(
                            list_name,
                            "وسایلی که برای این موقعیت نباید فراموش شوند",
                            show_reminder_lists,
                        ),

                        ft.Container(
                            padding=ft.Padding(20, 5, 20, 12),
                            content=ft.Row(
                                controls=[
                                    make_button(
                                        "＋ افزودن",
                                        add_item_click,
                                        bgcolor=BLUE_DARK,
                                        color=BLUE,
                                    ),

                                    make_button(
                                        "✎ تغییر نام",
                                        rename_list_click,
                                        bgcolor=CARD,
                                        color=TEXT,
                                    ),

                                    make_button(
                                        "حذف لیست",
                                        delete_list_click,
                                        bgcolor=RED_DARK,
                                        color=RED,
                                    ),
                                ],
                                spacing=8,
                                wrap=True,
                            ),
                        ),

                        ft.Container(
                            padding=ft.Padding(20, 0, 20, 30),
                            content=items_column,
                            expand=True,
                        ),
                    ],
                    expand=True,
                )
            )

            refresh_items()

        def refresh_lists():

            lists_column.controls.clear()

            all_lists = get_lists()

            query = (
                search_field.value.strip().lower()
                if search_field.value
                else ""
            )

            filtered_lists = []

            for reminder_list in all_lists:

                list_id, list_name = reminder_list

                if (
                    not query
                    or query in list_name.lower()
                ):
                    filtered_lists.append(
                        reminder_list
                    )

            if not filtered_lists:

                lists_column.controls.append(
                    ft.Container(
                        bgcolor=CARD,
                        border_radius=18,
                        padding=25,
                        content=ft.Column(
                            controls=[
                                ft.Text(
                                    "☷",
                                    size=35,
                                    color=MUTED_2,
                                ),
                                ft.Text(
                                    "لیستی پیدا نشد",
                                    color=TEXT,
                                    size=16,
                                    weight=ft.FontWeight.BOLD,
                                ),
                                ft.Text(
                                    "یک لیست جدید بساز یا عبارت دیگری جست‌وجو کن.",
                                    color=MUTED,
                                    size=12,
                                ),
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=7,
                        ),
                    )
                )

            else:

                for reminder_list in filtered_lists:

                    list_id, list_name = reminder_list

                    def open_list(
                        e,
                        current_list=reminder_list,
                    ):
                        show_list_items(current_list)

                    lists_column.controls.append(
                        ft.Container(
                            bgcolor=CARD,
                            border_radius=17,
                            padding=17,
                            on_click=open_list,
                            content=ft.Row(
                                controls=[
                                    ft.Container(
                                        width=46,
                                        height=46,
                                        bgcolor=ORANGE_DARK,
                                        border_radius=13,
                                        alignment=ft.Alignment.CENTER,
                                        content=ft.Text(
                                            "☷",
                                            color=ORANGE,
                                            size=20,
                                        ),
                                    ),

                                    ft.Column(
                                        controls=[
                                            ft.Text(
                                                list_name,
                                                color=TEXT,
                                                size=15,
                                                weight=ft.FontWeight.BOLD,
                                            ),
                                            ft.Text(
                                                "برای دیدن وسایل این لیست لمس کن",
                                                color=MUTED,
                                                size=11,
                                            ),
                                        ],
                                        spacing=4,
                                        expand=True,
                                    ),

                                    ft.Text(
                                        "←",
                                        color=MUTED,
                                        size=18,
                                    ),
                                ],
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                        )
                    )

            page.update()

        search_field.on_change = lambda e: refresh_lists()

        page.add(
            ft.Column(
                controls=[

                    make_page_header(
                        "فراموش نکردن وسایل",
                        "لیست‌های مخصوص سفر، فوتبال، سالن و کارهای مختلف",
                        show_home,
                    ),

                    ft.Container(
                        padding=ft.Padding(20, 5, 20, 12),
                        content=search_field,
                    ),

                    ft.Container(
                        padding=ft.Padding(20, 0, 20, 15),
                        content=make_button(
                            "＋  ساخت لیست جدید",
                            lambda e: show_add_reminder_list(),
                            bgcolor=ORANGE_DARK,
                            color=ORANGE,
                        ),
                    ),

                    ft.Container(
                        padding=ft.Padding(0, 0, 20, 30),
                        content=lists_column,
                        expand=True,
                    ),
                ],
                expand=True,
            )
        )

        refresh_lists()

    # =====================================================
    # HOME
    # =====================================================

    def show_home():

        clear_page()

        household_items = get_items()
        reminder_lists = get_lists()

        def create_card(
            icon,
            title,
            description,
            color_dark,
            color,
            on_click,
        ):

            card = ft.Container(
                bgcolor=CARD,
                border_radius=20,
                padding=18,
                on_click=on_click,
                content=ft.Column(
                    controls=[

                        ft.Container(
                            width=48,
                            height=48,
                            bgcolor=color_dark,
                            border_radius=14,
                            alignment=ft.Alignment.CENTER,
                            content=ft.Text(
                                icon,
                                color=color,
                                size=22,
                                weight=ft.FontWeight.BOLD,
                            ),
                        ),

                        ft.Container(height=4),

                        ft.Text(
                            title,
                            color=TEXT,
                            size=15,
                            weight=ft.FontWeight.BOLD,
                        ),

                        ft.Text(
                            description,
                            color=MUTED,
                            size=11,
                            max_lines=2,
                        ),
                    ],
                    spacing=5,
                ),
            )

            return card

        hero = ft.Container(
            margin=ft.Margin(20, 18, 20, 0),
            padding=ft.Padding(22, 22, 22, 22),
            border_radius=24,
            bgcolor=SURFACE,
            content=ft.Column(
                controls=[

                    ft.Row(
                        controls=[
                            ft.Container(
                                width=52,
                                height=52,
                                bgcolor=GREEN_DARK,
                                border_radius=16,
                                alignment=ft.Alignment.CENTER,
                                content=ft.Text(
                                    "⌂",
                                    color=GREEN,
                                    size=25,
                                ),
                            ),

                            ft.Column(
                                controls=[
                                    ft.Text(
                                        "وسایل خونه",
                                        color=TEXT,
                                        size=25,
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                    ft.Text(
                                        "همه چیز سر جای خودش.",
                                        color=GREEN,
                                        size=12,
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                ],
                                spacing=3,
                                expand=True,
                            ),
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),

                    ft.Container(height=8),

                    ft.Text(
                        "امروز دنبال چی می‌گردی؟",
                        color=MUTED,
                        size=13,
                    ),

                    ft.Row(
                        controls=[
                            ft.Container(
                                bgcolor=CARD,
                                border_radius=12,
                                padding=ft.Padding(12, 9, 12, 9),
                                content=ft.Row(
                                    controls=[
                                        ft.Text(
                                            str(len(household_items)),
                                            color=BLUE,
                                            size=16,
                                            weight=ft.FontWeight.BOLD,
                                        ),
                                        ft.Text(
                                            " وسیله",
                                            color=MUTED,
                                            size=11,
                                        ),
                                    ],
                                    spacing=2,
                                ),
                            ),

                            ft.Container(
                                bgcolor=CARD,
                                border_radius=12,
                                padding=ft.Padding(12, 9, 12, 9),
                                content=ft.Row(
                                    controls=[
                                        ft.Text(
                                            str(len(reminder_lists)),
                                            color=ORANGE,
                                            size=16,
                                            weight=ft.FontWeight.BOLD,
                                        ),
                                        ft.Text(
                                            " لیست",
                                            color=MUTED,
                                            size=11,
                                        ),
                                    ],
                                    spacing=2,
                                ),
                            ),
                        ],
                        spacing=8,
                    ),
                ],
                spacing=8,
            ),
        )

        cards = ft.Container(
            padding=ft.Padding(20, 18, 20, 20),
            content=ft.Column(
                controls=[

                    make_section_label(
                        "دسترسی سریع"
                    ),

                    ft.Row(
                        controls=[
                            create_card(
                                "⌕",
                                "جست‌وجوی وسایل",
                                "هر چیزی که قبلاً ثبت کردی پیدا کن",
                                BLUE_DARK,
                                BLUE,
                                lambda e: show_search(),
                            ),

                            create_card(
                                "+",
                                "اضافه کردن وسیله",
                                "یک وسیله جدید به خانه اضافه کن",
                                GREEN_DARK,
                                GREEN,
                                lambda e: show_add_item(),
                            ),
                        ],
                        spacing=10,
                    ),

                    ft.Row(
                        controls=[
                            create_card(
                                "✓",
                                "فراموش نکردن وسایل",
                                "لیست وسایلی که نباید جا بمونه",
                                ORANGE_DARK,
                                ORANGE,
                                lambda e: show_reminder_lists(),
                            ),

                            create_card(
                                "☷",
                                "ساخت لیست جدید",
                                "برای سفر، فوتبال، سالن و فعالیت‌ها",
                                BLUE_DARK,
                                BLUE,
                                lambda e: show_add_reminder_list(),
                            ),
                        ],
                        spacing=10,
                    ),
                ],
                spacing=13,
            ),
        )

        footer = ft.Container(
            padding=ft.Padding(20, 0, 20, 25),
            content=ft.Text(
                "ساده نگهش دار، یادت بمونه.  •  وسایل خونه",
                color=MUTED_2,
                size=10,
                text_align=ft.TextAlign.CENTER,
            ),
        )

        page.add(
            ft.Column(
                controls=[
                    hero,
                    cards,
                    footer,
                ],
                expand=True,
                scroll=ft.ScrollMode.AUTO,
            )
        )

        page.update()

    # =====================================================
    # START
    # =====================================================

    show_home()


if __name__ == "__main__":
    ft.run(main)