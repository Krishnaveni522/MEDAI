# Drug_Information.docx Format Guide

To import medicine data into MedAI, create a Microsoft Word document (.docx) with the following structure:

## Format Option 1: Table Format (Recommended)

Create a table with 2 columns:

| Drug | Instructions |
|------|--------------|
| Aspirin | Take 1 tablet (300-325mg) with water after meals. Do not exceed 4 tablets in 24 hours. Consult doctor if pain persists. |
| Paracetamol | Take 1-2 tablets (500mg each) every 4-6 hours. Maximum 8 tablets per day. Can be taken with or without food. |
| Amoxicillin | Take 1 capsule (500mg) three times daily for 5-7 days. Complete the full course. Take with food to reduce stomach upset. |

## Format Option 2: Colon Separated

```
Aspirin: Take 1 tablet (300-325mg) with water after meals. Do not exceed 4 tablets in 24 hours.

Paracetamol: Take 1-2 tablets (500mg each) every 4-6 hours. Maximum 8 tablets per day.

Amoxicillin: Take 1 capsule (500mg) three times daily for 5-7 days. Complete the full course.
```

## Format Option 3: Dash Separated

```
Aspirin - Take 1 tablet (300-325mg) with water after meals. Do not exceed 4 tablets in 24 hours.

Paracetamol - Take 1-2 tablets (500mg each) every 4-6 hours. Maximum 8 tablets per day.

Amoxicillin - Take 1 capsule (500mg) three times daily for 5-7 days. Complete the full course.
```

## Important Notes:

1. **First row**: If using table format, the first row with headers like "Drug", "Medicine", or "Name" will be automatically skipped
2. **Drug names**: Should be clear and consistent (include brand names and generic names if needed)
3. **Instructions**: Can be as detailed as needed (dosage, frequency, warnings, side effects)
4. **Duplicates**: If a drug name already exists in the database, it will be updated with new instructions
5. **Encoding**: Save the document in standard .docx format (Word 2007 or later)

## Example Content:

### Aspirin
- **Instructions**: Take 1 tablet (300-325mg) with water after meals. Do not exceed 4 tablets in 24 hours. Consult doctor if pain persists for more than 3 days.

### Paracetamol (Acetaminophen)
- **Instructions**: Take 1-2 tablets (500mg each) every 4-6 hours as needed. Maximum dose: 4000mg (8 tablets) per day. Can be taken with or without food. Overdose can cause liver damage.

### Amoxicillin
- **Instructions**: Take 1 capsule (500mg) three times daily for 5-7 days or as prescribed. Complete the full course even if symptoms improve. Take with food to reduce stomach upset. Notify doctor if rash develops.

### Ibuprofen
- **Instructions**: Take 1-2 tablets (200mg each) every 4-6 hours with food or milk. Do not exceed 1200mg (6 tablets) in 24 hours. Avoid if you have stomach ulcers or kidney problems.

### Cetirizine (Antihistamine)
- **Instructions**: Take 1 tablet (10mg) once daily in the evening. May cause drowsiness. Do not drive or operate machinery if affected. Can be taken with or without food.

## Tips for Best Results:

- Keep drug names short and clear
- Include both generic and brand names if commonly used
- Provide complete dosage information
- Include important warnings and side effects
- Mention any special instructions (e.g., "take with food", "avoid alcohol")
- Use clear, simple language

## After Creating Your File:

1. Save the document as `Drug_Information.docx`
2. Go to the Admin portal in MedAI
3. Click "Choose File" under "Import Drug Information from DOCX"
4. Select your file and click "Upload & Import"
5. The system will process and add all medicines to the database
