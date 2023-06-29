import z3

FolderSchema = z3.object({
    'id': z3.string(),
    'name': z3.string(),
    'type': z3.union([z3.literal('chat'), z3.literal('prompt')]),
})

FolderSchemaArray = z3.array(FolderSchema)
FolderType = z3.infer[FolderSchema]['type']
FolderInterface = z3.infer[FolderSchema]
