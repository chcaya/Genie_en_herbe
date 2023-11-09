# Genie_en_herbe
Hardware, Firmware et Software pour la fabrication d'un jeu de génie en herbe

## Imprimer les fichiers STL dans le dossier /CAD/STL<br />
8x Handle_V4_Body<br />
8x Handle_V4_Cover<br />
1x ESP32_CASE_V3_BASE<br />
1x ESP32_CASE_V3_COVER<br />

## Assemblage électrique
1- Connecter les grounds du ESP32 à 2 connecteurs Wago 5 pos<br />
2- Utiliser les connecteurs Wago 5 pos pour grounder tous les boutons (Fil noir)<br />
3- Connecter le fil rouge des boutons aux pins D15, D4, D16, D17 pour l'équipe 1<br />
4- Connecter le fil rouge des boutons aux pins D13, D14, D27, D26 pour l'équipe 2<br />
5- Passer les fils rouge et noir dans le trou de la poignée avant de souder les boutons sur ceux-ci<br />
6- Souder les fils rouge et noir sur les boutons<br />

## Assemblage mécanique
1- Utiliser les vis M3x16mm et les écrous pour assembler les poignées<br />
*Attention de faire sortir les fils par le trou central prévu à cet effet avant de visser solidement l'assemblage<br />
2- Utiliser les vis M3x25mm et les inserts pour assembler le boitier de jeu<br />
*Attention de faire sortir les fils par les 8 trous sur les côtés du boitier avant de visser solidement l'assemblage<br />

## Script code embarqué
1- Connecter l'ESP32 à l'ordinateur à l'aide du fil micro-USB (Valider la reconnaissance par l'ordinateur via le gestionnaire de périphériques)<br />
*Si celui-ci n'est pas reconnu, télécharger les drivers à partir de "/MCU/DEV/CP210x_Windows_Drivers_with_Serial_Enumeration/CP210xVCPInstaller_x86.exe"<br />
2- Lancer le script "MCU/UploadScript.exe" pour télécharger le code sur l'ESP32<br />
3- Attendre que tous les fichiers (bootloader.bin, partitions.bin et firmware.bin) soient correctement téléchargés avant d'interrompre le processus<br />

## Application GUI
1- Lancer l'application "/GUI/GEH_GUI.exe" lorsque l'ESP32 est connecté à l'ordinateur<br />
2- Sélectionner les équipes à l'aide des menus déroulants<br />
3- Lorsqu'un joueur appuie sur son bouton, le GUI indique le numéro et l'équipe du joueur<br />
4- Pour passer au prochain tour, il est possible d'appuyer sur le bouton "Reset" avec la souris ou simplement sur "Enter" avec le clavier
