/// <reference types="node" />

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import Ajv from 'ajv';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const ajv = new Ajv({ allErrors: true });

function compileAndValidate(entityName: string, rawDir: string, schemaPath: string, outputFile: string) {
    console.log(__filename);
    console.log(__dirname);
    
    const schemaContent = fs.readFileSync(schemaPath, 'utf-8');
    const validate = ajv.compile(JSON.parse(schemaContent));
    
    const db: Record<string, unknown> = {};
    const files = fs.readdirSync(rawDir).filter(file => file.endsWith('.json'));

    files.forEach(file => {
        const filePath = path.join(rawDir, file);
        const fileContent = fs.readFileSync(filePath, 'utf-8');
        const parsedJson = JSON.parse(fileContent);

        const isValid = validate(parsedJson);

        if (!isValid) {
            console.error(`\nValidation Failed in: ${file}`);
            console.error(ajv.errorsText(validate.errors));
            process.exit(1);
        }

        Object.assign(db, parsedJson);
    });

    const outputDir = path.dirname(outputFile);
    if (!fs.existsSync(outputDir)) {
        fs.mkdirSync(outputDir, { recursive: true });
    }

    fs.writeFileSync(outputFile, JSON.stringify(db, null, 2));
    console.log(`Compiled ${files.length} ${entityName} into ${outputFile}`);
}

const configs = [
    {
        name: 'Races',
        rawDir: path.join(__dirname, '../src/assets/resources/races'),
        schema: path.join(__dirname, '../src/assets/schemas/race_data_schema.json'),
        output: path.join(__dirname, '../src/assets/resources/races.json')
    },
    {
        name: 'Subraces',
        rawDir: path.join(__dirname, '../src/assets/resources/subraces'),
        schema: path.join(__dirname, '../src/assets/schemas/subrace_data_schema.json'),
        output: path.join(__dirname, '../src/assets/resources/subraces.json')
    },
    {
        name: 'Traits',
        rawDir: path.join(__dirname, '../src/assets/resources/traits'),
        schema: path.join(__dirname, '../src/assets/schemas/trait_data_schema.json'),
        output: path.join(__dirname, '../src/assets/resources/traits.json')
    }
];

console.log('Starting Data Compilation Pipeline...');
console.log(__filename);
console.log(__dirname);
configs.forEach(config => {
    console.log(config.rawDir);
    console.log(fs.existsSync(config.rawDir))
    console.log(config.schema);
    console.log(fs.existsSync(config.schema))
    if (fs.existsSync(config.rawDir) && fs.existsSync(config.schema)) {
        compileAndValidate(config.name, config.rawDir, config.schema, config.output);
    } else {
        console.warn(  `Skipping ${config.name}: Directory or Schema not found.`);
    }
});
