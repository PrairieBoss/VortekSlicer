"""Execute the welcome identity script against shipped translated text."""
from pathlib import Path
import shutil
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[2]


@unittest.skipUnless(shutil.which("node"), "Node.js is not available")
class TestWelcomeBranding(unittest.TestCase):
    def run_javascript(self, checks):
        harness = r'''
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const context = {};
vm.runInNewContext(fs.readFileSync('resources/web/data/text.js', 'utf8'), context);
vm.runInNewContext(fs.readFileSync('resources/web/guide/1/1.js', 'utf8'), context);
function page(locale) {
    const nodes = {
        Title: {textContent: context.LangText[locale].t1},
        STip: {textContent: context.LangText[locale].t2},
        credit: {textContent: 'Derived from OrcaSlicer'}
    };
    for (const node of Object.values(nodes)) {
        Object.defineProperty(node, 'innerHTML', {set() {throw new Error('Identity must be text, never HTML');}});
    }
    context.document = {getElementById: id => nodes[id] || null};
    context.TranslatePage = () => {
        nodes.Title.textContent = context.LangText[locale].t1;
        nodes.STip.textContent = context.LangText[locale].t2;
    };
    return nodes;
}
''' + checks
        result = subprocess.run(["node", "-e", harness], cwd=ROOT,
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_product_name_preserves_all_shipped_welcome_translations(self):
        self.run_javascript(r'''
for (const locale of Object.keys(context.LangText)) {
    const nodes = page(locale);
    context.ApplyApplicationName('VortekSlicer');
    for (const id of ['Title', 'STip']) {
        assert.ok(nodes[id].textContent.includes('VortekSlicer'), locale + ':' + id);
        assert.ok(!nodes[id].textContent.includes('Orca'), locale + ':' + id);
    }
    assert.equal(nodes.credit.textContent, 'Derived from OrcaSlicer');
}
const french = page('fr_FR'); context.ApplyApplicationName('VortekSlicer');
assert.equal(french.Title.textContent, 'Bienvenue sur VortekSlicer');
assert.equal(french.STip.textContent, 'VortekSlicer sera configuré en plusieurs étapes. Commençons !');
const turkish = page('tr_TR'); context.ApplyApplicationName('VortekSlicer');
assert.equal(turkish.STip.textContent, 'VortekSlicer birkaç adımda kurulacaktır. Hadi başlayalım!');
''')

    def test_native_identity_survives_both_translation_event_orders(self):
        for native_first in (True, False):
            with self.subTest(native_first=native_first):
                self.run_javascript("const nativeFirst = " + str(native_first).lower() + ";" + r'''
const nodes = page('fr_FR');
if (nativeFirst) context.ApplyApplicationName('VortekSlicer');
context.InitWelcome();
if (!nativeFirst) context.ApplyApplicationName('VortekSlicer');
assert.equal(nodes.Title.textContent, 'Bienvenue sur VortekSlicer');
assert.equal(nodes.STip.textContent, 'VortekSlicer sera configuré en plusieurs étapes. Commençons !');
context.InitWelcome();
assert.equal(nodes.Title.textContent, 'Bienvenue sur VortekSlicer');
''')

    def test_upstream_and_invalid_identity_preserve_existing_text(self):
        self.run_javascript(r'''
for (const value of ['OrcaSlicer', '', null, undefined, 42, {}]) {
    const nodes = page('en');
    context.ApplyApplicationName(value);
    assert.equal(nodes.Title.textContent, context.LangText.en.t1);
    assert.equal(nodes.STip.textContent, context.LangText.en.t2);
}
context.document = {getElementById: () => null};
assert.doesNotThrow(() => context.ApplyApplicationName('VortekSlicer'));
''')

    def test_identity_is_literal_text_and_the_page_loads_the_script(self):
        self.run_javascript(r'''
const nodes = page('en');
const name = '<img src=x onerror=alert(1)>$&';
context.ApplyApplicationName(name);
assert.equal(nodes.Title.textContent, 'Welcome to ' + name);
assert.equal(nodes.STip.textContent, name + " will be setup in several steps. Let's start!");
''')
        html = (ROOT / "resources/web/guide/1/index.html").read_text(encoding="utf-8")
        self.assertIn('src="1.js"', html)
        self.assertIn('onLoad="InitWelcome()"', html)


if __name__ == "__main__":
    unittest.main()
