const fs = require('fs');

const lemmas = JSON.parse(fs.readFileSync('ru-lemmas.json'));

const result = {};

for (let index = 0; index < lemmas.length; index++) {
  const entry = lemmas[index];

  const { word, info } = entry;

  info.forEach((inf) => {
    const gender = [];

    const { pos, senses, sounds, categories, head_templates } = inf;

    const aspectInfo = { pf: '', impf: '' };

    if (pos === 'verb' && head_templates) {
      head_templates.forEach((head) => {
        // if (word == 'дать') console.log(head);

        const { args } = head;
        const aspect = args['2'];
        let { pf, impf } = args;

        if (pf) pf = pf.replace(/́/g, '');
        if (impf) impf = impf.replace(/́/g, '');

        if (aspect == 'impf') {
          aspectInfo['impf'] = word;
          aspectInfo['pf'] = pf;
        } else if (aspect == 'pf') {
          aspectInfo['pf'] = word;
          aspectInfo['impf'] = impf;
        }
      });
    }

    let nonLemmaAndLemma = false;

    if (categories) {
      if (
        categories.includes('Russian lemmas') &&
        categories.includes('Russian non-lemma forms')
      )
        nonLemmaAndLemma = true;

      if (pos === 'noun') {
        if (categories.includes('Russian feminine nouns'))
          gender.push('feminine');
        if (categories.includes('Russian masculine nouns'))
          gender.push('masculine');
        if (categories.includes('Russian neuter nouns')) gender.push('neuter');
      }
    }

    let { forms } = inf;

    let ipa = '';

    if (sounds) {
      sounds.forEach((entry) => {
        const entIPA = entry.ipa;

        if (entIPA && !ipa) ipa = entIPA;
      });
    }

    let defs = [];

    senses.forEach((sense) => {
      const { form_of, raw_glosses, categories } = sense;

      if (categories) {
        if (
          categories.includes('Russian lemmas') &&
          categories.includes('Russian non-lemma forms')
        )
          nonLemmaAndLemma = true;

        if (pos === 'noun') {
          if (categories.includes('Russian feminine nouns'))
            gender.push('feminine');
          if (categories.includes('Russian masculine nouns'))
            gender.push('masculine');
          if (categories.includes('Russian neuter nouns'))
            gender.push('neuter');
        }
      }

      if (raw_glosses) {
        raw_glosses.forEach((gloss) => {
          let junkDef = false;

          if (pos === 'character') junkDef = true;

          // remove romanization info
          // ex: гото́вить (gotóvitʹ) => гото́вить
          if (/\sof\s.+?\(.+?\)$/.test(gloss) && !nonLemmaAndLemma) {
            gloss = gloss.replace(/\s\(.+?\)$/, '');
          }

          gloss = gloss.replace(/́/g, '');

          // remove the form info provided by wiktionary
          // since we already have form data in the forms array
          if (/\sof\s.+?\(.+?\)$/.test(gloss) && nonLemmaAndLemma)
            junkDef = true;

          if (/^The Cyrillic letter/.test(gloss)) junkDef = true;

          if (!junkDef) defs.push(gloss);
        });
      }
    });

    if (defs.length > 0) {
      let outputForms = [];

      if (forms) {
        forms.forEach((f) => {
          let { form, tags } = f;

          form = form.replace(/́/g, '');

          if (form) {
            if (/[ЁёА-я]/.test(form) && !/stem/.test(form))
              outputForms.push({ form, tags });
          }
        });
      }

      const alternates = {};

      outputForms.forEach((entry) => {
        let { form } = entry;

        form = form.replace(/́/g, '');

        if (/ё/.test(form)) {
          const alternateForm = form.replace(/ё/g, 'е');

          if (!result[alternateForm]) {
            result[alternateForm] = [
              {
                ipa: '',
                pos: 'alternate-form',
                defs: [`Alternate spelling of ${form}`],
                forms: [],
                gender: [],
              },
            ];

            alternates[alternateForm] = [form];
          } else if (alternates[alternateForm]) {
            if (!alternates[alternateForm].includes(form)) {
              result[alternateForm].push({
                ipa: '',
                pos: 'alternate-form',
                defs: [`Alternate spelling of ${form}`],
                forms: [],
                gender: [],
              });

              alternates[alternateForm].push(form);
            }
          }
        }
      });

      if (!result[word])
        result[word] = [
          { ipa, pos, defs, forms: outputForms, gender, aspectInfo },
        ];
      else
        result[word].push({
          ipa,
          pos,
          defs,
          forms: outputForms,
          gender,
          aspectInfo,
        });
    }
  });
}

// Uncomment to see some results

// console.log('проверка\n', result['проверка'][0]);
// console.log('кимчхи\n', result['кимчхи']);
// console.log(
//   'бережёного бог бережёт\n',
//   result['бережёного бог бережёт'][0].forms,
// );
// console.log('прийти\n', result['прийти'][0]);

fs.writeFileSync('ru-en-wiktionary-dict.json', JSON.stringify(result));
