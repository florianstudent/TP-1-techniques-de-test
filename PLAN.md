### PINTO Florian

Monsieur, veuillez m'excuser pour le retard, en fait je n'avais pas mon groupe dans la section "Déclaration du groupe" parce que je pensais que c'était automatique, et donc les zones de rendus étaient toutes fermées.
Comme vous m'aviez dit que nous avions jusqu'a la séance prochaine  pour rendre ce fichier, j'ai cru que les rendus seraient ouverts à partir de la prochaine séance.


# Plan de tests
Ce plan de tests est composé de 6 parties :
- Partie 1 : Tests unitaire
- Partie 2 : Tests de conversion binaire
- Partie 3 : Tests de l'API du triangulator
- Partie 4 : Tests de la communication entre le Triangulator et le PointSetManager
- Partie 5 : Tests de performance
- Partie 6 : Tests de qualité


## Partie 1 : Tests unitaire
Cette batterie de tests vise à vérifier la logique de calcul de la triangulation, sans prendre en compte l'API du Triangulator ainsi que le PointSetManager

Test 1 : test de triangulation avec un ensemble de points simple. Vérifier que la triangulation obtenue est correcte pour un ensemble de points permettant de former un ou plusieurs triangles.

Test 2 : test avec un nombre de points insuffisant. Vérifier que le cas d'un ensemble contenant moins de 3 points est correctement géré, puisqu'aucun triangle ne peut être formé.

Test 3 : test avec des points dégénérés. Vérifier le comportement avec des points alignés ou des points dupliqués, qui peuvent empêcher la création d'une triangulation valide.

Test 4 : test de cohérence de la triangulation obtenue. Vérifier que les indices des sommets des triangles correspondent bien aux points d'entrée et que les triangles produits sont valides.


## Partie 2 : Tests de conversion binaire
Cette batterie de tests vise à vérifier que les données manipulées par le Triangulator sont correctement converties entre leur représentation interne et le format binaire.

Test 1 : test de la sérialisation et désérialisation des PointSet. Vérifier le nombre de points, les coordonnées et le respect du format binaire défini par l'API.

Test 2 : test de données binaires invalides ou incohérentes. Vérifier que des données ne respectant pas le format attendu ne sont pas interprétées comme un PointSet valide.

Test 3 : test de la sérialisation et désérialisation des Triangles. Vérifier le nombre de sommets, le nombre de triangles et les trois indices de chaque triangle.

Test 4 : test d'une conversion aller-retour. Vérifier qu'une sérialisation suivie d'une désérialisation conserve intégralement les données initiales.

Test 5 : test de cas limites. Vérifier le comportement avec des données ne contenant aucun sommet et/ou aucun triangle.


## Partie 3 : Tests de l'API du triangulator
Cette batterie de tests vise à vérifier le bon comportement HTTP du triangulator, en mettant de coté l'algorithme de triangulation.

Test 1 : test d'une requête valide avec un PointSetID existant. Vérifier l'envoi d'une réponse 200 contenant un Triangles au format binaire attendu, si la requête est valide.

Test 2 : test d'un PointSetID au format invalide. Vérifier l'envoi une réponse 400 contenant un code et un message si le PointSetID a bien un format invalide.

Test 3 : test d'un PointSetID inexistant. Vérifier l'envoi d'une réponse 404 contenant un code et un message si le PointSetID n'existe pas.

Test 4 : test d'un échec de triangulation. Vérifier l'envoi d'une réponse 500 contenant le code TRIANGULATION_FAILED et le message associé si la triangulation échoue.

Test 5 : test d'une indisponibilité du PointSetManager. Vérifier l'envoi d'une réponse 503 contenant un code et un message si le PointSetManager est indisponible.


## Partie 4 : Tests de la communication entre le Triangulator et le PointSetManager
Cette batterie de tests vise à vérifier que le Triangulator et le PointSetManager communiquent correctement et que le Triangulator gère correctement les différentes réponses du PointSetManager. Il ne s'agit cependant pas de tester le PointSetManager lui même.

Test 1 : test de la récupération d'un PointSet existant. Vérifier que le Triangulator récupère correctement le PointSet auprès du PointSetManager et utilise les données reçues pour effectuer la triangulation.

Test 2 : test d'un PointSet inexistant. Vérifier que le Triangulator renvoie une réponse 404 contenant un code et un message lorsque le PointSetManager indique que le PointSet demandé n'existe pas.

Test 3 : test d'une indisponibilité du PointSetManager. Vérifier que le Triangulator renvoie une réponse 503 contenant un code et un message lorsque la communication avec le PointSetManager échoue ou que celui-ci est indisponible.

Test 4 : test d'une réponse invalide du PointSetManager. Vérifier que le Triangulator gère correctement un PointSet reçu qui ne respecte pas le format binaire attendu.


## Partie 5 - Tests de performance
Cette batterie de tests vise à mesurer les performances du système sur les opérations de triangulation et de conversion des données binaires. Le but est de mesurer leur temps d'exécution pour différentes tailles de données.

Test 1 : mesure du temps d'exécution de la triangulation. Vérifier le temps nécessaire pour trianguler des ensembles de points de tailles différentes.

Test 2 : mesure du temps de conversion des PointSet. Vérifier le temps nécessaire pour sérialiser et désérialiser des PointSet de tailles différentes.

Test 3 : mesure du temps de conversion des Triangles. Vérifier le temps nécessaire pour sérialiser et désérialiser des Triangles contenant un nombre différent de sommets et de triangles.

Test 4 : répétition des mesures. Répéter les tests plusieurs fois pour chaque catégorie de volume de données (faible, moyen important, très important), afin d'obtenir des mesures de performance représentatives.


## Partie 6 - Tests de qualité
Cette batterie de tests vise à vérifier la qualité globale du projet à l'aide des bibliothèques présentes dans le fichier dev_requirements.txt (coverage, ruff, pdoc3). Cette vérification doit couvrir les tests, la couverture de code, le linting et la documentation.

Test 1 : vérification de l'exécution de tous les tests. Vérifier que l'ensemble des tests des parties 1 à 4 s'exécute correctement.

Test 2 : vérification de la couverture de code. Vérifier que la couverture obtenue avec coverage est suffisante (>= 85% selon les normes de SonarQube) et que les parties importantes du projet sont couvertes par les tests.

Test 3 : vérification du respect des règles de qualité du code. Vérifier que le projet respecte les règles définies avec ruff et qu'aucune erreur de linting n'est détectée.

Test 4 : vérification de la documentation. Vérifier que la documentation du projet peut être générée correctement avec pdoc3 et qu'elle couvre les éléments importants du code.

Test 5 : vérification des commandes make du projet. Vérifier que les commandes test, unit_test, perf_test, coverage, lint et doc prévues par le sujet fonctionnent correctement.


















