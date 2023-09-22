from odoo import api, http, fields, models, tools, modules
from odoo.addons.base.models.ir_module import assert_log_admin_access
from odoo.addons.base.models.ir_module import Module
from odoo.tools.parse_version import parse_version

class ModuleInherit(models.Model):
    _inherit = "ir.module.module"

    @assert_log_admin_access
    @api.model
    def update_list(self):
        res = [0, 0]  # [update, add]
        default_version = modules.adapt_version('1.0')
        known_mods = self.with_context(lang=None).search([])
        known_mods_names = {mod.name: mod for mod in known_mods}

        # iterate through detected modules and update/create them in db
        for mod_name in modules.get_modules():
            mod = known_mods_names.get(mod_name)
            terp = self.get_module_info(mod_name)
            values = self.get_values_from_terp(terp)

            if mod:
                updated_values = {}
                for key in values:
                    old = getattr(mod, key)
                    if (old or values[key]) and values[key] != old:
                        updated_values[key] = values[key]
                if terp.get('installable', True) and mod.state == 'uninstallable':
                    updated_values['state'] = 'uninstalled'
                if parse_version(terp.get('version', default_version)) > parse_version(
                        mod.latest_version or default_version):
                    res[0] += 1
                if updated_values:
                    mod.write(updated_values)
            else:
                mod_path = modules.get_module_path(mod_name)
                if not mod_path or not terp:
                    continue
                state = "uninstalled" if terp.get('installable', True) else "uninstallable"
                mod = self.create(dict(name=mod_name, state=state, **values))
                res[1] += 1

            mod._update_dependencies(terp.get('depends', []), terp.get('auto_install'))
            mod._update_exclusions(terp.get('excludes', []))
            mod._update_category(terp.get('category', 'Uncategorized'))

            mod.icon_image = ''
            if mod.id:
                path = modules.module.get_module_icon(mod.name)
            else:
                path = ''
            if path:
                mod.write({'icon': path})

        return res

    Module.update_list = update_list


