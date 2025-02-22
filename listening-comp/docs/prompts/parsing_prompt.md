Vous êtes un expert dans la création de matériel d'apprentissage du français langue étrangère de très haute qualité, spécifiquement dans le style des épreuves de compréhension orale du TCF (Test de Connaissance du Français). Votre performance sera jugée sur la précision et l'adéquation au style TCF de votre production. **Un indexage incorrect de la réponse correcte est une erreur critique et sera lourdement pénalisée.**

Votre tâche est de traiter un transcript YouTube en français et d'en extraire des ensembles dialogue-question-réponses adaptés à la pratique de la compréhension orale pour le TCF. Pour chaque dialogue, vous devrez générer une question dans le style TCF et créer quatre options de réponses à choix multiples plausibles, également dans le style TCF.

**Entrée :**

Vous recevrez un transcript YouTube en français sous forme de texte brut. Ce transcript représente l'audio d'une conversation ou discussion en français.

**Tâches Essentielles et Exigences Critiques :**

1.  **Segmentation du dialogue avec priorité à la Fluidité et au Sens Logique, et Identification précise des Locuteurs :**
    *   Divisez le transcript en segments de dialogue **fluides, logiques et naturels**.  Priorisez le **sens de la conversation** et les **pauses naturelles** pour créer des échanges qui imitent une conversation réelle.  **Évitez absolument de créer des tours de parole excessivement longs et monolithiques qui ne reflètent pas le rythme d'un dialogue oral.**
    *   **Analysez attentivement le déroulement logique de la conversation.**  Assurez-vous que chaque segment de dialogue représente un échange cohérent et compréhensible dans un contexte conversationnel réel. Le dialogue doit progresser de manière logique et intuitive pour un auditeur.
    *   **Identifiez avec précision les locuteurs et leurs tours de parole.** Soyez extrêmement attentif aux indices de changement de locuteur dans le transcript. Utilisez les noms (ex : Marie, Pierre), les indications de genre ('Homme', 'Femme') si disponibles, ou des identifiants génériques ('Locuteur 1', 'Locuteur 2', etc.) en veillant à ce que chaque locuteur identifié corresponde bien à une personne distincte dans la conversation. **Ne confondez pas les locuteurs et n'attribuez pas le même identifiant à des personnes différentes.**
    *   Pour chaque tour de parole, extrayez l'identifiant du locuteur et le **texte français corrigé, grammaticalement parfait, et rendu fluide et naturel**. **Corrigez impérativement toute erreur de transcription, toute phrase maladroite ou peu naturelle** pour que chaque phrase extraite soit digne d'une conversation entre locuteurs natifs.  Le dialogue produit doit être **parfaitement compréhensible et avoir du sens** pour un francophone.

2.  **Extraction et Formulation de Questions Style TCF :**
    *   Au sein de chaque segment de dialogue fluide et logique, identifiez la ou les phrases qui constituent une question dans le style des épreuves de compréhension orale du TCF. La question se situe typiquement après un court échange dialogué.  Extrayez ou formulez une question directement pertinente par rapport au dialogue.
    *   **Formulez les questions dans un style approprié au TCF. Privilégiez les questions qui testent l'inférence, la compréhension de l'intention du locuteur et le sens implicite, et non seulement la simple mémorisation de faits explicites.** Utilisez des amorces de questions typiques du TCF, telles que :
        *   "Qu'est-ce qu'on apprend sur...?"
        *   "De quoi s'agit-il dans... ?"
        *   "Quel est le sujet de... ?"
        *   "Que fait/dit... ?"
        *   "Pourquoi... ?" (à utiliser avec parcimonie, et assurez-vous de distracteurs excellents).
        *   "À quoi s'intéresse...?"

3.  **Génération d'Options de Réponses de Haute Qualité Style TCF (4 Options avec Distracteurs Nuancés) :**
    *   Pour chaque dialogue et question, générez **quatre (4)** options de réponses plausibles **en français grammaticalement parfait et naturel**, ressemblant étroitement aux options à choix multiples du TCF.
    *   **Une option DOIT être clairement, définitivement et sans ambiguïté la *réponse correcte***, basée *uniquement* sur les informations explicitement ou implicitement fournies dans le segment de dialogue.
    *   **Les trois (3) autres options DOIVENT être des distracteurs nuancés de haute qualité, essentiels au style TCF.** Les distracteurs doivent :
        *   Être **plausibles** et pertinents par rapport au *thème* et au *contexte* du dialogue.
        *   Tester des **points subtils de compréhension**, des nuances de vocabulaire et des compétences d'inférence.
        *   Être **directement liés aux détails spécifiques du dialogue**, et pas seulement des possibilités générales.
        *   **Éviter d'être manifestement faux, absurdes ou trop facilement éliminés.**
        *   **Exemple de BONS distracteurs :** Options partiellement vraies mais manquant une nuance clé du dialogue, options liées au thème mais pas à la situation spécifique du dialogue, options représentant des erreurs de compréhension ou des inférences erronées communes pour un apprenant de langue.
        *   **Exemple de MAUVAIS distracteurs (À ÉVITER) :** Options complètement hors sujet, options grammaticalement incorrectes, options factuellement fausses dans la culture générale, options simplement absurdes ou ridicules.

4.  **Identification Précise de l'Index de la Réponse Correcte - CRITIQUE !**
    *   Pour chaque ensemble de quatre options de réponses, **identifiez avec soin et précision l'index (0, 1, 2 ou 3) de l' *unique réponse définitivement correcte***.
    *   **Vérifiez et revérifiez que l' `index_réponse_correcte` pointe *toujours* et sans exception vers l'option de réponse réellement correcte dans le tableau `answers`, en utilisant un indexage basé sur 0.**  Un `index_réponse_correcte` incorrect sera considéré comme un échec majeur.

5.  **Sortie JSON Structurée :** Formattez votre sortie sous forme de **liste JSON**. Chaque élément de la liste doit être un objet JSON représentant un ensemble dialogue-question-réponses. L'objet JSON doit avoir les clés **en anglais** et la structure exacte suivantes, avec les *valeurs* en **français fluide et grammaticalement parfait** :

    ```json
    [
      {
        "dialogue": [          // **Dialogue est une liste de tours de parole**
          ["Speaker 1", "Bonjour, comment vas-tu ?"],  // Chaque tour de parole est une liste [Identifiant Locuteur, Texte]
          ["Speaker 2", "Très bien, merci. Et toi ?"]
        ],
        "question": "...",     // Question style TCF (français)
        "answers": [          // Tableau de 4 options de réponses (français)
          "option 1",
          "option 2",
          "option 3",
          "option 4"
        ],
        "correct_answer_index": 0, // Index (basé sur 0) de la réponse correcte (entier : 0, 1, 2 ou 3)
        "speakers_info": ["Speaker 1", "Speaker 2"] // (Optionnel, Identifiants des locuteurs)
      },
      // ... d'autres objets JSON pour chaque ensemble dialogue-question-réponses extrait
    ]
    ```
    **Note :** Le champ `"dialogue"` est désormais une **liste de listes/tuples**. Assurez-vous que tout le texte français est fluide et d'une grammaire impeccable.

**Exemple de Sortie Attendue (JSON - avec clés en anglais, valeurs en français, dialogue structuré, et style TCF) :**

```json
[
  {
    "dialogue": [
      ["Locuteur 1", "Salut Marie, ça va ? Tu n'as pas l'air en forme."],
      ["Marie", "Non, je suis fatiguée ce matin. J'ai passé une très mauvaise nuit."],
      ["Marie", "Les voisins du dessous ont fait la fête jusqu'à 3 heures du matin."],
      ["Locuteur 1", "Tu n'es pas descendu les voir ?"],
      ["Marie", "Non, j'ai hesité, mais je crois que la prochaine fois je leur demanderai de mettre un peu moins fort"]
    ],
    "question": "Qu'est-ce qui explique la fatigue de Marie ?",
    "answers": [
      "Un excès de travail récent.",
      "Une insomnie due au stress.",
      "Le bruit de la fête des voisins.",
      "Un léger problème de santé passager."
    ],
    "correct_answer_index": 2,
    "speakers_info": ["Locuteur 1", "Marie"]
  },
  {
    "dialogue": [
      ["Locuteur 1", "Au fait, des nouvelles pour ton entretien d'embauche de la semaine dernière ?"],
      ["Locuteur 2", "Rien encore.  Je consulte ma boîte mail chaque matin."],
      ["Locuteur 1", "Tu devrais peut-être les relancer, non ?"],
      ["Locuteur 2", "Oui, sûrement. On m'avait dit qu'il y avait beaucoup de candidats."]
    ],
    "question": "De quoi parlent les deux locuteurs ?",
    "answers": [
      "De l'organisation d'un voyage.",
      "De l'attente d'une réponse pour un emploi.",
      "De la préparation d'une réunion importante.",
      "Des difficultés de communication avec une entreprise."
    ],
    "correct_answer_index": 1,
    "speakers_info": ["Locuteur 1", "Locuteur 2"]
  }
]
```

Considérations Importantes :

- Fluidité et Grammaire Française : Votre production DOIT être en français fluide, grammaticalement parfait et naturel, adapté à des apprenants de langue.
- Style TCF et Niveau de Difficulté : Visez un niveau de difficulté et un style de questions/réponses appropriés à la compréhension orale du TCF (niveau A2-B1).
- La Précision est Primordiale : Surtout pour correct_answer_index. Vérifiez absolument tout.
- Priorité au Sens Logique : Assurez-vous que les dialogues créés ont un sens logique et imitent une conversation naturelle en français.
Processus :

Vous allez recevoir le transcript français. Traitez-le en suivant toutes les tâches et exigences détaillées ci-dessus. Retournez votre sortie sous forme d'une seule chaîne JSON, formatée comme une liste d'objets JSON, correspondant exactement à la structure présentée dans la section "Exemple de sortie attendue". Assurez-vous que tout le texte produit (dialogues, questions, réponses) est en français fluide et grammaticalement impeccable.

Transcript à Traiter :

[Musique]
salue marie ça va tu n'as pas
forme non je suis fatigué ce matin j'ai
passé une très mauvaise nuit
les voisins du dessous on fait la fête
jusqu'à 3 heures du matin qui n'est pas
descendu les bords non j'ai hésité mais
je crois que la prochaine fois je leur
dirai de mettre un peu moins fort
pourquoi marine est elle pas en forme
au fait est ce que tu as eu des
nouvelles de la candidature qui a envoyé
la semaine dernière n'ont toujours pas
je surveille ma boite mail tous les
matins tu ne crois pas que tu devrais
les rappeler peut-être oui la personne
que j'ai eu la première fois m'a indiqué
qu'il y avait beaucoup de candidats pour
ce poste
c'est peut-être pour ça qu'il met un peu
de temps à te répondre sans doute je
tends la fin de la semaine et je les
rappelle
quel est l'objet de la conversation
3
allo pierre je t'appelle pour te dire
que je risque d'être en retard au
travail ce matin
qu'est ce qui t'arrive c'est une fuite
d'eau dans la cuisine et je n'arrive pas
à joindre le plombier
ok je comprends ne t'en fais pas nous
commencerons la réunion sans toi
rejoins-nous quand tu peux merci je fais
le plus rapidement possible
quel est l'objet de la conversation
vous partez ou en vacances cet été à
vrai dire je ne sais pas si nous
pourrons partir ah bon pourquoi
eh bien je viens de commencer un nouveau
travail je ne suis pas sûr qu'on
m'accorde des congés cette année
quiconque pose la question à ton
employeur je peux essayer mais je n'ai
pas tellement envie d'aborder le sujet
des vacances alors que je viens d'être
embauchés je comprends
pourquoi la personne ne peut pas partir
en vacances
la nouvelle bibliothèque située dans
l'espace culturel du centre ville a été
inaugurée le 8 octobre dernier
six bénévoles se relaient trois fois par
semaine pour accueillir les visiteurs et
les guider dans leur choix de lecture
cette ouverture était très attendu tant
par la population que par les élus
après de longs mois de travaux et
quelques retards de chantier des
habitants vont enfin pouvoir profiter de
l'immense collection d'ouvragés acquis
par la ville les livres pourront être
empruntés gratuitement partout les moins
de 18 ans
de quoi parle l'article
on sait que les français ne sont pas
très doués en anglais ce qu'on sait
moins c'est que les femmes sont plus à
l'aise avec l'anglais que les hommes et
que c'est à paris que le niveau
d'anglais est le meilleur malgré tout la
france reste l'une des plus mauvaises
élèves au niveau européen bien loin des
pays du nord tels que la norvège et le
danemark
de quoi parle l'article
1
non
non
[Musique]