from django.utils.html import format_html
from tuitse import THAU_JI, LIAN_JI, KHIN_SIANN_JI
from 臺灣言語工具.基本物件.公用變數 import 敢是拼音字元


def tuitse_html(kiamtsa_tinliat):
    html = ''
    htmlsu = ''
    kam_hing_ai_lian = False
    kam_ting_tsit_hing_si_lomaji = False

    kam_im_ai_lian = False
    kam_ting_tsit_im_si_lomaji = False
    for ji in kiamtsa_tinliat:
        # Kuat-tīng Tsit jī ê hîng ài liân-jī-hû--bô
        try:
            kam_hing_si_lomaji = 敢是拼音字元(ji[0][-1])
        except IndexError:
            kam_hing_si_lomaji = False

        if kam_hing_si_lomaji and kam_ting_tsit_hing_si_lomaji:
            kam_hing_ai_lian = True
        else:
            kam_hing_ai_lian = False

        kam_ting_tsit_hing_si_lomaji = kam_hing_si_lomaji

        # Kuat-tīng Tsit jī ê im ài liân-jī-hû--bô
        try:
            kam_im_si_lomaji = 敢是拼音字元(ji[1][-1])
        except IndexError:
            kam_im_si_lomaji = False

        if kam_im_si_lomaji and kam_ting_tsit_im_si_lomaji:
            kam_im_ai_lian = True
        else:
            kam_im_ai_lian = False

        kam_ting_tsit_im_si_lomaji = kam_im_si_lomaji

        if ji[2] == THAU_JI:
            # Thòo sû ê html
            if htmlsu:
                html += "<ruby>{}</ruby>".format(htmlsu)
            # Html tîng-lâi
            htmlsu = _sng_ji_html(ji)
            continue

        tiauhu = ''
        if ji[2] == LIAN_JI:
            tiauhu = '-'
        elif ji[2] == KHIN_SIANN_JI:
            tiauhu = '--'
        else:
            raise('一定愛設定頭字、連字、a̍h-sī輕聲')

        if kam_im_ai_lian:
            htmlsu += "<rb>{}</rb>".format(tiauhu)
        else:
            htmlsu += "<rb>&nbsp;</rb>"

        if kam_hing_ai_lian:
            htmlsu += "<rt>{}</rt>".format(tiauhu)
        else:
            htmlsu += "<rt></rt>"

        htmlsu += _sng_ji_html(ji)
    # Thòo bué sû ê html
    html += "<ruby>{}</ruby>".format(htmlsu)
    return format_html(html)


def _sng_ji_html(ji):
    if ji[3]:
        return "<rb>{}</rb><rt>{}</rt>".format(ji[1], ji[0])
    if ji[1]:
        return "<rb class='fail'>{}</rb><rt class='fail'>{}</rt>".format(
            ji[1], ji[0])
    return "<rb class='fail'>&nbsp;&nbsp;</rb><rt class='fail'>{}</rt>".format(
        ji[0])
