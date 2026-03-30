type BrainstormPart = 'II' | 'III';
type BrainstormEntryType = 'IDEA' | 'LIB';
type BrainstormPriority = 'HIGH' | 'MED' | 'LOW' | 'PARKED';
type BrainstormStatus =
    | 'SEED'
    | 'EXPLORING'
    | 'CANDIDATE'
    | 'PROMOTED'
    | 'REJECTED'
    | 'PARKED'
    | 'SUPERSEDED';
type BrainstormCategory =
    | 'CAT-ARCH'
    | 'CAT-DAG'
    | 'CAT-VIZ'
    | 'CAT-CRUD'
    | 'CAT-VALID'
    | 'CAT-STORE'
    | 'CAT-LIFE'
    | 'CAT-EXT'
    | 'CAT-UX'
    | 'CAT-DIST'
    | 'CAT-AI'
    | 'CAT-TEST'
    | 'CAT-MISC';
type BrainstormTier =
    | 'XPD'
    | 'SIL'
    | 'GPCL'
    | 'FCL'
    | 'CL'
    | 'SAL'
    | 'ICL'
    | 'CDL'
    | 'ISL';
type BrainstormExtension =
    | 'E1'
    | 'E2'
    | 'E3'
    | 'E4'
    | 'E5'
    | 'E6'
    | 'E7'
    | 'E8'
    | 'E9';
type BrainstormRelevance = BrainstormTier | BrainstormExtension;
type BrainstormLanguage = 'Python' | 'JavaScript' | 'Rust' | 'Go' | 'Other';
type BrainstormLicense =
    | 'MIT'
    | 'Apache-2.0'
    | 'BSD-2-Clause'
    | 'BSD-3-Clause'
    | 'ISC'
    | 'MPL-2.0'
    | 'LGPL'
    | 'Other';
type BrainstormCommercialUse = 'YES' | 'CONDITIONAL' | 'NO';
type BrainstormMaintenance = 'ACTIVE' | 'MAINTAINED' | 'SLOW' | 'ARCHIVED';
type BrainstormMaturity = 'EXPERIMENTAL' | 'STABLE' | 'MATURE' | 'LEGACY';
type BrainstormVerdict = 'CANDIDATE' | 'UNDER_REVIEW' | 'ACCEPTED' | 'REJECTED' | 'PARKED';

interface BrainstormCommonEntry {
    entry_type: BrainstormEntryType;
    entry_id: string;
    title: string;
    category: BrainstormCategory;
    priority: BrainstormPriority;
    status: BrainstormStatus;
    authored_by: string;
    /** ISO 8601 date string: YYYY-MM-DD */
    authored_date: string;
    /** ISO 8601 date string: YYYY-MM-DD */
    revised_date: string;
    description: string;
    detail: string;
    open_questions: string[];
    tags: string[];
    ddr_relevance: BrainstormRelevance[];
    references: string[];
}

interface BrainstormIdeaEntry extends BrainstormCommonEntry {
    entry_type: 'IDEA';
    motivation: string;
    prior_art: string;
    ddr_constraints: string;
    risks: string;
    dependencies: string[];
}

interface BrainstormLibraryEntry extends BrainstormCommonEntry {
    entry_type: 'LIB';
    repository: string;
    language: BrainstormLanguage;
    license: BrainstormLicense;
    commercial_use: BrainstormCommercialUse;
    latest_release: string;
    maintenance: BrainstormMaintenance;
    install_size_kb: number | string;
    maturity: BrainstormMaturity;
    verdict: BrainstormVerdict;
    rejection_reason: string;
}

type BrainstormEntry = BrainstormIdeaEntry | BrainstormLibraryEntry;

interface PartRegistryRow {
    part_id: string;
    short_title: string;
    status: string;
}

interface BrainstormDocumentMetadata {
    document_id: string;
    base_version: string;
    status: string;
    owner: string;
    /** ISO 8601 date string: YYYY-MM-DD */
    created: string;
    /** ISO 8601 date string: YYYY-MM-DD */
    last_revised: string;
    schema: string;
    reference_source: string;
}

interface BrainstormDocument {
    metadata: BrainstormDocumentMetadata;
    part_registry: PartRegistryRow[];
    part_ii_entries: BrainstormIdeaEntry[];
    part_iii_entries: BrainstormLibraryEntry[];
}
