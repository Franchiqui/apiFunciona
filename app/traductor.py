import deepl

def traductor_func(translate_text, target_lang):
    auth_key = "a4341cbe-a8bd-4ac2-97e4-6bce2574cf8a:fx"  # Reemplaza con tu clave
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(translate_text, target_lang=target_lang)
    return result.text



