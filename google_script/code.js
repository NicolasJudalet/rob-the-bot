// ------------------------------
// --- CopyPasteNewFormValues ---
// ------------------------------
// - Copy pastes new values inserted
// by Google Form from SkillsDB
// sheet to SkillsFinder sheet
// - Triggered everytime new values
// are inserted (cf project's triggers)

function copyPasteFormulas(e) {
  const SKILLS_DB_SHEET_NAME = "Skills DB";

  const SKILL_AREA_RANGE_NAME = "SkillAreaRange";
  const WISH_AREA_RANGE_NAME = "WishAreaRange";
  const SKILLS_LEVELS_FIRST_ROW_RANGE = "SkillsLevelsFirstRowRange";

  const dbSheet = SpreadsheetApp.getActive().getSheetByName(
    SKILLS_DB_SHEET_NAME
  );

  // Add skills formulas to inserted line
  const skillAreaRange = dbSheet.getRange(SKILL_AREA_RANGE_NAME);
  const skillDestinationRange = dbSheet.getRange(
    e["range"]["rowStart"],
    skillAreaRange.getColumn(),
    1,
    skillAreaRange.getLastColumn()
  );
  skillAreaRange.copyTo(skillDestinationRange);

  // Add wishes formulas to inserted line
  const wishAreaRange = dbSheet.getRange(WISH_AREA_RANGE_NAME);
  const wishDestinationRange = dbSheet.getRange(
    e["range"]["rowStart"],
    wishAreaRange.getColumn(),
    1,
    wishAreaRange.getLastColumn()
  );
  wishAreaRange.copyTo(wishDestinationRange);

  // Convert skills levels
  const skillsLevelsFirstRowRange = dbSheet.getRange(
    SKILLS_LEVELS_FIRST_ROW_RANGE
  );
  const insertedRow = e["range"]["rowEnd"];
  const numberOfDataRows = 1 + insertedRow - skillsLevelsFirstRowRange.getRow();
  const numberOfSkillsColumns =
    1 +
    skillsLevelsFirstRowRange.getLastColumn() -
    skillsLevelsFirstRowRange.getColumn();
  const skillsLevelsRange = dbSheet.getRange(
    skillsLevelsFirstRowRange.getRow(),
    skillsLevelsFirstRowRange.getColumn(),
    numberOfDataRows,
    numberOfSkillsColumns
  );
  skillsLevelsRange.setValues(convertSkillsLabelsIntoLevels(skillsLevelsRange));

  // Copy all correctly formatted values to SkillsFinder sheet
  duplicateFormValues(
    insertedRow,
    e["range"]["columnStart"],
    e["range"]["columnEnd"]
  );
}

// ---------------------------
// --- DuplicateFormValues ---
// ---------------------------
// Copy pastes the values from
// Skills DB to Skills Finder

function duplicateFormValues(
  insertedRangeRow,
  insertedRangeFirstColumn,
  insertedRangeLastColumn
) {
  // Constants
  const SKILLS_DB_SHEET_NAME = "Skills DB";
  const SKILLS_FINDER_SHEET_NAME = "Skills Finder";

  const DB_TAB_FIRST_DATA_ROW_RANGE_NAME = "DbTabFirstDataRowRange";
  const SF_TAB_FIRST_DATA_ROW_RANGE_NAME = "SfTabFirstDataRowRange";
  const DB_TAB_HEADERS_RANGE_NAME = "DbTabHeadersRange";
  const SF_TAB_HEADERS_RANGE_NAME = "SfTabHeadersRange";

  // Get each sheet's first row of data
  const dbSheet = SpreadsheetApp.getActive().getSheetByName(
    SKILLS_DB_SHEET_NAME
  );
  const skillsFinderSheet = SpreadsheetApp.getActive().getSheetByName(
    SKILLS_FINDER_SHEET_NAME
  );

  const dbTabFirstDataRowRange = dbSheet.getRange(
    DB_TAB_FIRST_DATA_ROW_RANGE_NAME
  );
  const sfTabFirstDataRowRange = skillsFinderSheet.getRange(
    SF_TAB_FIRST_DATA_ROW_RANGE_NAME
  );

  // Get origin and destination ranges and copy paste
  const numberOfFormDataRows =
    1 + insertedRangeRow - dbTabFirstDataRowRange.getRow();
  const numberOfFormDataColumns =
    1 + insertedRangeLastColumn - insertedRangeFirstColumn;
  const formValuesRange = dbSheet.getRange(
    dbTabFirstDataRowRange.getRow(),
    insertedRangeFirstColumn,
    numberOfFormDataRows,
    numberOfFormDataColumns
  );
  const duplicateDataDestinationRange = skillsFinderSheet.getRange(
    sfTabFirstDataRowRange.getRow(),
    sfTabFirstDataRowRange.getColumn(),
    numberOfFormDataRows,
    numberOfFormDataColumns
  );
  formValuesRange.copyTo(duplicateDataDestinationRange);

  // Copy headers as values (prevents bug when sorting using the filtered views)
  const dbHeadersRange = dbSheet.getRange(DB_TAB_HEADERS_RANGE_NAME);
  const sfHeadersRange = skillsFinderSheet.getRange(SF_TAB_HEADERS_RANGE_NAME);
  dbHeadersRange.copyTo(sfHeadersRange, { contentsOnly: true });
}

// -------------------------------------
// --- ConvertSkillsLabelsIntoLevels ---
// -------------------------------------
// Helper that converts the skills labels into int levels
// Ex: "1 - Je peux contribuer en autonomie" --> 1 (int)

function convertSkillsLabelsIntoLevels(skillsLevelsRange) {
  return skillsLevelsRange.getValues().map(function (row) {
    return row.map(function (skillLabel) {
      return typeof skillLabel === "string"
        ? Number(skillLabel.substring(0, 1))
        : skillLabel;
    });
  });
}

function onOpen() {
  const title = "Important : Ne pas écrire directement dans le document";
  const messageLine1 =
    "Les données de ce document sont actualisées automatiquement par Google Form.";
  const messageLine2 =
    "Le document contient des formules qui pourraient cesser de fonctionner si vous modifiez le contenu des cellules.";
  const messageLine3 =
    "La manière correcte d'utiliser 'SkillsFinder' (via les filtered views) est expliquées dans l'onglet 'How To'.";
  const message = [messageLine1, messageLine2, messageLine3].join("\n");

  const ui = SpreadsheetApp.getUi();

  ui.alert(title, message, ui.ButtonSet.OK);
}
