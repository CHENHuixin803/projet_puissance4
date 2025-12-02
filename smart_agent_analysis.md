## Tâche 3.8 : Comparaison des performances
### 1. Taux de victoire : Intelligent vs Aléatoire sur 100 parties
En exécutant la fonction de test dix fois,  il y a eu trois fois un taux de victoire de 100 %,  cinq fois un taux de victoire de 99 %,  une fois un taux de victoire de 98 %,  et une fois un taux de victoire de 96 %.

### 2. Efficacité de la stratégie : Quelles règles se déclenchent le plus souvent ?
La règle de préférence pour le centre est celle qui est déclenchée le plus souvent.
### 3. Cas d'échec : Quand votre agent intelligent perd-il ?
Voici un exemple où SmartAgent a perdu :
SmartAgent LOST this game!
Move history for this losing game:
  Step 1: player_0 played column 3
  Step 2: player_1 played column 5
  Step 3: player_0 played column 3
  Step 4: player_1 played column 3
  Step 5: player_0 played column 3
  Step 6: player_1 played column 5
  Step 7: player_0 played column 3
  Step 8: player_1 played column 2
  Step 9: player_0 played column 3
  Step 10: player_1 played column 2
  Step 11: player_0 played column 2
  Step 12: player_1 played column 2
  Step 13: player_0 played column 2
  Step 14: player_1 played column 5
  Step 15: player_0 played column 5
  Step 16: player_1 played column 5
  Step 17: player_0 played column 2
  Step 18: player_1 played column 5
  Step 19: player_0 played column 4
  Step 20: player_1 played column 4

Après que RandomAgent a joué dans la colonne 3 au quatrième coup, il ne restait plus que trois cases libres dans cette colonne. Même si SmartAgent continuait à privilégier cette colonne centrale, cela ne pouvait plus mener à une position gagnante. Cependant, SmartAgent a tout de même continué à jouer prioritairement dans cette colonne.   
De plus, le dernier coup de SmartAgent a créé une occasion de victoire immédiate pour l’adversaire, alors que ses règles ne prévoient aucune vérification visant à éviter de « donner » une position gagnante à l’adversaire.  

（在第四步RandomAgent下在第三列后，第三列只剩三个空格，SmartAgent即使继续优先选择中间列下棋也不能取得胜利，但是SmartAgent仍然继续优先选择第三列；其次，SmartAgent的最后一步制造了对手下一步立刻获胜的机会，而它的规则里没有“避免给对手送必胜”的检查。）
### 3. Améliorations : Qu'est-ce qui pourrait le rendre plus fort ?
Ajouter une règle pour éviter les « coups suicidaires » : avant de jouer un coup, SmartAgent simule le résultat de ce coup ; si, après ce coup, l’adversaire peut réaliser immédiatement un alignement de quatre dans une colonne, alors ce coup est considéré comme un « coup suicidaire » et doit absolument être évité.  

（增添规则不要下“自杀步” ：SmartAgent 在尝试某个落子之前，先模拟一下：如果这个落子之后，对手某一列可以立刻4连，那么这个落子是“自杀步”，绝对不能下。）