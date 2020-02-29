from core_module.builder.Builder import Builder, TemplateBuilder

class Director:

    def buildTemplate(self, builder):
        builder.build_header()
        builder.build_script()
        return builder.get_product()
