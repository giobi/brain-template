# Brain Coherence Check

Controllo settimanale per verificare che il brain non si contraddica come un politico in campagna elettorale.

---

## 🎯 Frequenza

**Settimanale** (al più tardi) - o quando noti che hai scritto la stessa cazzata in 3 posti diversi.

---

## 🔍 Scope

Verificare contraddizioni e inconsistenze in:
- **boot/** (identity.md, personal.md, rules.md)
- **tools/** (tutti i README.md e index.md)
- Altri file critici di configurazione

---

## 📋 Cosa Controllare

### 1. Contraddizioni tra file

Quando un file dice X e un altro dice "no vabbè, facciamo Y":
- boot/identity.md dice metodo X, tools/README.md dice metodo Y
- Regole che si contraddicono tra documenti
- Informazioni duplicate ma inconsistenti

**Esempio classico**:
```
gmail/index.md: "Usa SOLO Claude direct"
gmail-queue-system.md: "Usa Circus con Gemini"
→ CONTRADDIZIONE TOTALE 🔥
```

### 2. Info obsolete

Roba che era vera nel 2015 ma ora è archeologia:
- Riferimenti a tool/script eliminati
- Procedure deprecate ancora documentate
- Esempi che usano metodi vecchi
- "Usa Python 2.7" (cristo [REDATTO])

### 3. Token thresholds

Verificare che i boot files non siano diventati dei romanzi:
```bash
wc -c /home/claude/brain/boot/*.md
```

**Soglie**:
- identity.md < 12k char
- personal.md < 20k char
- rules.md < 8k char
- Totale < 40k char

Se superi: è ora di fare pulizia, non di alzare la soglia (furbo eh?).

### 4. Cross-references

Link che puntano al nulla cosmico:
- Wikilinks rotti `[[file-che-non-esiste]]`
- Riferimenti a file inesistenti
- Path cambiati non aggiornati
- "Vedi tools/telegram/" (che telegram? Non esiste porcoddio)

---

## 🔧 Come Eseguire

**Comando**: "Fai controllo coerenza brain"

**Processo**:
1. Leggi boot/identity.md, boot/personal.md, boot/rules.md
2. Leggi tutti i tools/*/index.md e tools/*/README.md
3. Cerca contraddizioni (metodi diversi per stessa task)
4. Cerca riferimenti obsoleti (script eliminati, procedure vecchie)
5. Report contraddizioni trovate + suggerimenti fix
6. **Non fixare automaticamente** - proporre modifiche per approvazione

**Output atteso**:

```markdown
## Contraddizioni trovate:

1. **gmail/index.md:7 vs gmail-queue-system.md:15**
   - Problema: Metodi processing contraddicono
   - Suggerimento: Chiarire quando usare quale metodo

2. **cron/README.md:38**
   - Problema: Dice "3x al giorno" ma crontab fa "ogni ora"
   - Suggerimento: Aggiornare README con frequency corretta

3. **tools/telegram/**
   - Problema: Referenziato ma non esiste
   - Suggerimento: Rimuovere reference o creare directory
```

---

## ⏰ Quando Triggera

- **Manualmente**: User richiede "controllo coerenza"
- **Proattivamente**: Dopo grosse modifiche a boot/ o tools/
- **Reminder**: Se passata 1+ settimana da ultimo controllo

**Ultimo controllo**: 2025-10-29 (refactoring boot)

---

## 🎯 Obiettivo

Evitare che il brain diventi come il codice legacy: dove nessuno sa perché funziona ma tutti hanno paura di toccarlo.

**Mantra**: "Una fonte di verità" > "Tre versioni della stessa bugia"

---

*Keep it clean, keep it consistent, keep it sane.*
