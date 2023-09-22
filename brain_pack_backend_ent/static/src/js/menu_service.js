/** @odoo-module **/

import { browser } from "@web/core/browser/browser";
import { registry } from "@web/core/registry";
import { session } from "@web/session";

const loadMenusUrl = `/web/webclient/load_menus`;
const menuServiceRegistry = registry.category("services");

function makeFetchLoadMenus() {
    const cacheHashes = session.cache_hashes;
    let loadMenusHash = cacheHashes.load_menus || new Date().getTime().toString();
    return async function fetchLoadMenus(reload) {
        if (reload) {
            loadMenusHash = new Date().getTime().toString();
        } else if (odoo.loadMenusPromise) {
            return odoo.loadMenusPromise;
        }
        const res = await browser.fetch(`${loadMenusUrl}/${loadMenusHash}`);

        if (!res.ok) {
            throw new Error("Error while fetching menus");
        }
        return res.json();
    };
}

function makeMenus(env, menusData, fetchLoadMenus) {
    let currentAppId;
    return {
        getAll() {
            return Object.values(menusData);
        },
        getApps() {
            return this.getMenu("root").children.map((mid) => this.getMenu(mid));
        },
        getMenu(menuID) {
            return menusData[menuID];
        },
        getCurrentApp() {
            if (!currentAppId) {
                return;
            }
            var target_tag = '.o_navbar_apps_menu a.main_link[data-menu='+currentAppId+']'
            $(target_tag).addClass('active');
            if($(target_tag).hasClass('dropdown-btn')){
                var ultag = $(target_tag).parent().find('.header-sub-menus')
                $(ultag).addClass('show');
            }
            return this.getMenu(currentAppId);
        },
        getMenuAsTree(menuID) {
            const menu = this.getMenu(menuID);
            if (!menu.childrenTree) {
                menu.childrenTree = menu.children.map((mid) => this.getMenuAsTree(mid));
            }
            return menu;
        },
        async selectMenu(menu) {
            menu = typeof menu === "number" ? this.getMenu(menu) : menu;
            if (!menu.actionID) {
                return;
            }
            await env.services.action.doAction(menu.actionID, { clearBreadcrumbs: true });
            this.setCurrentMenu(menu);
            if (!$('body').hasClass('o_home_menu_background')){
                $('body').css("background-image", "")
            }
        },
        setCurrentMenu(menu) {
            menu = typeof menu === "number" ? this.getMenu(menu) : menu;
            /* if (menu && menu.xmlid) {
                // var xmlid = menu.xmlid.split('.')[0]
                var xmlid = menu.xmlid
                console.log("xmlid==========",xmlid);
                if (xmlid == 'website.menu_website_configuration' || xmlid == 'website.menu_website_preview'){
                    $('body').attr("iswebsite", true)
                    // $('body').addClass('top_menu_horizontal').removeClass('top_menu_vertical');
                } else {
                    $('body').removeAttr("iswebsite")
                    // $('body').addClass('top_menu_vertical').removeClass('top_menu_horizontal');
                }
            } */
            if (menu && menu.appID !== currentAppId) {
                currentAppId = menu.appID;
                env.bus.trigger("MENUS:APP-CHANGED");
                // FIXME: lock API: maybe do something like
                // pushState({menu_id: ...}, { lock: true}); ?
                env.services.router.pushState({ menu_id: menu.id }, { lock: true });
            }
        },
        async reload() {
            if (fetchLoadMenus) {
                menusData = await fetchLoadMenus(true);
                env.bus.trigger("MENUS:APP-CHANGED");
            }
        },
    };
}

export const menuService = {
    dependencies: ["action", "router"],
    async start(env) {
        const fetchLoadMenus = makeFetchLoadMenus();
        const menusData = await fetchLoadMenus();
        return makeMenus(env, menusData, fetchLoadMenus);
    },
};

menuServiceRegistry.remove("menu");
menuServiceRegistry.add("menu", menuService);