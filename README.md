# دليل SUR-ARDL — SUR-ARDL Interactive Guide

منصة تعليمية تفاعلية بالعربية تشرح منهجية **SUR-ARDL**: من أساسيات السلاسل
الزمنية، إلى نظام زيلنر (1962)، إلى اختبار الحدود لبيساران وشين وسميث (2001)،
وصولًا إلى الدمج الذي قدّمته ورقة أريف وفوروكا (2026).

An interactive Arabic-language guide to the SUR-ARDL methodology — seemingly
unrelated regressions with autoregressive distributed lag dynamics — built
with Streamlit.

**إعداد: الدكتور مروان رودان · Dr Merwan Roudane**

---

## ماذا تحتوي المنصة؟

| القسم | المحتوى |
|---|---|
| **الأساسيات** | السكون، رتب التكامل، التكامل المشترك، نموذج تصحيح الخطأ |
| **المنهجيتان** | نظام SUR لزيلنر 1962، واختبار الحدود لـ PSS 2001 |
| **الدمج** | منهجية SUR-ARDL 2026 ولماذا تنجح |
| **الرياضيات** | الاشتقاق الكامل بأرقام المعادلات كما في الورقة الأصلية |
| **التطبيق** | الاختبارات القبلية، التقدير، الاختبارات البعدية، قراءة النتائج |
| **المرجع** | دليل أمر `surardl` في Stata، أخطاء شائعة، معجم المصطلحات |

تتضمّن المنصة رسومًا تفاعلية ومحاكاة حيّة وأنيميشن يوضّح آلية تصحيح الخطأ،
وتخطيطات Mermaid لمسار التحليل.

## التشغيل محليًا

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## الحزمة المرافقة في Stata

المجلد `stata/` يحوي الأمر **`surardl`** الذي ينفّذ المنهجية كاملة:

```stata
ssc install surardl
help surardl
```

يشمل التقدير بـ FGLS، واختبار الحدود بأربعة مصادر للقيم الحرجة (PSS 2001،
Narayan 2005، محاكاة، وإعادة معاينة)، ومعاملات الأجل الطويل بفترات دلتا
وFieller وBootstrap، والاختبارات العابرة للمعادلات، وجداول ورسومًا بمستوى
النشر الأكاديمي.

## البنية

```
streamlit_app.py        نقطة الدخول والتنقّل
app_pages/              صفحات الدليل السبع عشرة
lib/ui.py               التخطيط من اليمين إلى اليسار والبطاقات
lib/viz.py              الرسوم والمحاكاة والأنيميشن
.streamlit/config.toml  السمة الفاتحة متعددة الألوان
stata/                  حزمة surardl لـ Stata
```

## المراجع الأساسية

- Arif & Furuoka (2026) — [doi:10.21203/rs.3.rs-9237078/v1](https://doi.org/10.21203/rs.3.rs-9237078/v1)
- Zellner (1962) — [doi:10.1080/01621459.1962.10480664](https://doi.org/10.1080/01621459.1962.10480664)
- Pesaran, Shin & Smith (2001) — [doi:10.1002/jae.616](https://doi.org/10.1002/jae.616)
- McNown, Sam & Goh (2018) — [doi:10.1080/00036846.2017.1366643](https://doi.org/10.1080/00036846.2017.1366643)

قائمة كاملة داخل المنصة، في صفحة **المراجع والمصطلحات**.

## الترخيص

MIT

---

**Dr Merwan Roudane** · merwanroudane920@gmail.com ·
[github.com/merwanroudane](https://github.com/merwanroudane)
