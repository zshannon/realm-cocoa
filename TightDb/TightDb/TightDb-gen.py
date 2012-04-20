import sys
from Cheetah.Template import Template

templateDef = """#slurp
#compiler-settings
commentStartToken = %%
directiveStartToken = %
#end compiler-settings
//
//  TightDb.h
//  TightDB
//

#import "OCTable.h"
#import "OCQuery.h"
#import "OCCursor.h"

%for $i in range($max_cols)
%set $num_cols = $i + 1
#undef TDB_TABLE_IMPL_${num_cols}
#define TDB_TABLE_IMPL_${num_cols}(TableName%slurp
%for $j in range($num_cols)
, CType${j+1}, CName${j+1}%slurp
%end for
) \\
@implementation TableName##_Cursor \\
    { \\
    %for $j in range($num_cols)
        OCAccessor *_##CName${j+1}; \\
    %end for
    } \\
    -(id)initWithTable:(OCTable *)table ndx:(size_t)ndx; \\
    { \\
    self = [super initWithTable:table ndx:ndx]; \\
    if (self) { \\
    %for $j in range($num_cols)        
    _##CName${j+1} = [[OCAccessor alloc] initWithCursor:self columnId:${j}]; \\
    %end for        
    } \\
    return self; \\
    } \\
%for $j in range($num_cols)
    -(tdbOCType##CType${j+1})CName${j+1} \\
    { \\
        return [_##CName${j+1} get##CType${j+1}]; \\
    } \\
    -(void)set##CName${j+1}:(tdbOCType##CType${j+1})value \\
    { \\
    [_##CName${j+1} set##CType${j+1}:value]; \\
    } \\
%end for
@end \\
@implementation TableName##_##Query \\
%for $j in range($num_cols)
@synthesize CName${j+1} = _CName${j+1}; \\
%end for
-(id)init \\
{ \\
    self = [super init]; \\
    if (self) { \\
%for $j in range($num_cols)
        _CName${j+1} = [[TableName##QueryAccessor##CType${j+1} alloc] initWithColumn:${j} query:self]; \\
%end for
    } \\
    return self; \\
} \\
-(TableName##_##Query *)group \\
{ \\
    [super group]; \\
    return self; \\
} \\
-(TableName##_##Query *)or \\
{ \\
    [super or]; \\
    return self; \\
} \\
-(TableName##_##Query *)endgroup \\
{ \\
    [super endgroup]; \\
    return self; \\
} \\
-(TableName##_##Query *)subtable:(size_t)column \\
{ \\
    [super subtable:column]; \\
    return self; \\
} \\
-(TableName##_##Query *)parent \\
{ \\
    [super parent]; \\
    return self; \\
} \\
@end \\
@implementation TableName##QueryAccessorInt \\
-(TableName##_##Query *)equal:(size_t)value \\
{ \\
    return (TableName##_##Query *)[super equal:value]; \\
} \\
-(TableName##_##Query *)notEqual:(size_t)value \\
{ \\
    return (TableName##_##Query *)[super notEqual:value]; \\
} \\
-(TableName##_##Query *)greater:(int64_t)value \\
{ \\
    return (TableName##_##Query *)[super greater:value]; \\
} \\
-(TableName##_##Query *)less:(int64_t)value \\
{ \\
    return (TableName##_##Query *)[super less:value]; \\
} \\
-(TableName##_##Query *)between:(int64_t)from to:(int64_t)to \\
{ \\
    return (TableName##_##Query *)[super between:from to:to]; \\
} \\
@end \\
@implementation TableName##QueryAccessorBool \\
-(TableName##_##Query *)equal:(BOOL)value \\
{ \\
    return (TableName##_##Query *)[super equal:value]; \\
} \\
@end \\
@implementation TableName##QueryAccessorString \\
-(TableName##_##Query *)equal:(NSString *)value caseSensitive:(BOOL)caseSensitive \\
{ \\
    return (TableName##_##Query *)[super equal:value caseSensitive:caseSensitive]; \\
} \\
-(TableName##_##Query *)notEqual:(NSString *)value caseSensitive:(BOOL)caseSensitive \\
{ \\
    return (TableName##_##Query *)[super notEqual:value caseSensitive:caseSensitive]; \\
} \\
-(TableName##_##Query *)beginsWith:(NSString *)value caseSensitive:(BOOL)caseSensitive \\
{ \\
    return (TableName##_##Query *)[super beginsWith:value caseSensitive:caseSensitive]; \\
} \\
-(TableName##_##Query *)endsWith:(NSString *)value caseSensitive:(BOOL)caseSensitive \\
{ \\
    return (TableName##_##Query *)[super endsWith:value caseSensitive:caseSensitive]; \\
} \\
-(TableName##_##Query *)contains:(NSString *)value caseSensitive:(BOOL)caseSensitive \\
{ \\
    return (TableName##_##Query *)[super contains:value caseSensitive:caseSensitive]; \\
} \\
@end \\
@implementation TableName \\
%for $j in range($num_cols)
@synthesize CName${j+1} = _##CName${j+1}; \\
%end for
\\
-(id)initWithBlock:(TopLevelTableInitBlock)block \\
{ \\
    self = [super init]; \\
    if (self) { \\
        if (block) block(self); \\
%for $j in range($num_cols)
        [self registerColumn:COLTYPE##CType${j+1} name:[NSString stringWithUTF8String:#CName${j+1}]]; \\
%end for
\\
%for $j in range($num_cols)
        _##CName${j+1} = [[OCColumnProxy##CType${j+1} alloc] initWithTable:self column:${j}]; \\
%end for
    } \\
    return self; \\
} \\
-(id)init \\
{ \\
    self = [super init]; \\
    if (self) { \\
%for $j in range($num_cols)
        [self registerColumn:COLTYPE##CType${j+1} name:[NSString stringWithUTF8String:#CName${j+1}]]; \\
%end for
\\
%for $j in range($num_cols)
        _##CName${j+1} = [[OCColumnProxy##CType${j+1} alloc] initWithTable:self column:${j}]; \\
%end for
    } \\
    return self; \\
} \\
-(void)add##%slurp
%for $j in range($num_cols)
CName${j+1}:(tdbOCType##CType${j+1})CName${j+1} %slurp
%end for
\\
{ \\
    const size_t ndx = [self count]; \\
%for $j in range($num_cols)
    [self insert##CType${j+1}:${j} ndx:ndx value:CName${j+1}]; \\
%end for
    [self insertDone]; \\
} \\
-(void)insertAtIndex:(size_t)ndx %slurp
%for $j in range($num_cols)
CName${j+1}:(tdbOCType##CType${j+1})CName${j+1} %slurp
%end for
\\
{ \\
%for $j in range($num_cols)
    [self insert##CType${j+1}:${j} ndx:ndx value:CName${j+1}]; \\
%end for
    [self insertDone]; \\
} \\
-(TableName##_##Query *)getQuery \\
{ \\
    return [[TableName##_##Query alloc] init]; \\
} \\
-(TableName##_Cursor *)add \\
{ \\
    return [[TableName##_Cursor alloc] initWithTable:self ndx:[self addRow]]; \\
} \\
-(TableName##_Cursor *)objectAtIndex:(size_t)ndx \\
{ \\
    return [[TableName##_Cursor alloc] initWithTable:self ndx:ndx]; \\
} \\
-(TableName##_Cursor *)back \\
{ \\
    return [[TableName##_Cursor alloc] initWithTable:self ndx:[self count]-1]; \\
} \\
@end

%end for

%for $i in range($max_cols)
%set $num_cols = $i + 1
#undef TDB_TABLE_DEF_${num_cols}
#define TDB_TABLE_DEF_${num_cols}(TableName%slurp
%for $j in range($num_cols)
, CType${j+1}, CName${j+1}%slurp
%end for
) \\
@interface TableName##_Cursor : OCCursorBase \\
    %for $j in range($num_cols)
    @property tdbOCType##CType${j+1} CName${j+1}; \\
    %end for
    %for $j in range($num_cols)
    -(tdbOCType##CType${j+1})CName${j+1}; \\
    -(void)set##CName${j+1}:(tdbOCType##CType${j+1})value; \\
    %end for
@end \\
@class TableName##_##Query; \\
@interface TableName##QueryAccessorInt : OCXQueryAccessorInt \\
-(TableName##_##Query *)equal:(size_t)value; \\
-(TableName##_##Query *)notEqual:(size_t)value; \\
-(TableName##_##Query *)greater:(int64_t)value; \\
-(TableName##_##Query *)less:(int64_t)value; \\
-(TableName##_##Query *)between:(int64_t)from to:(int64_t)to; \\
@end \\
@interface TableName##QueryAccessorBool : OCXQueryAccessorBool \\
-(TableName##_##Query *)equal:(BOOL)value; \\
@end \\
@interface TableName##QueryAccessorString : OCXQueryAccessorString \\
-(TableName##_##Query *)equal:(NSString *)value caseSensitive:(BOOL)caseSensitive; \\
-(TableName##_##Query *)notEqual:(NSString *)value caseSensitive:(BOOL)caseSensitive; \\
-(TableName##_##Query *)beginsWith:(NSString *)value caseSensitive:(BOOL)caseSensitive; \\
-(TableName##_##Query *)endsWith:(NSString *)value caseSensitive:(BOOL)caseSensitive; \\
-(TableName##_##Query *)contains:(NSString *)value caseSensitive:(BOOL)caseSensitive; \\
@end \\
@interface TableName##_##Query : OCQuery \\
%for $j in range($num_cols)
@property(nonatomic, strong) TableName##QueryAccessor##CType${j+1} *CName${j+1}; \\
%end for
-(TableName##_##Query *)group; \\
-(TableName##_##Query *)or; \\
-(TableName##_##Query *)endgroup; \\
-(TableName##_##Query *)subtable:(size_t)column; \\
-(TableName##_##Query *)parent; \\
@end \\
@interface TableName : OCTopLevelTable \\
%for $j in range($num_cols)
@property(nonatomic, strong) OCColumnProxy##CType${j+1} *CName${j+1}; \\
%end for
-(void)add##%slurp
%for $j in range($num_cols)
%if 0 < $j
%echo ' '
%end if
CName${j+1}:(tdbOCType##CType${j+1})CName${j+1}%slurp
%end for
; \\
-(void)insertAtIndex:(size_t)ndx%slurp
%for $j in range($num_cols)
 CName${j+1}:(tdbOCType##CType${j+1})CName${j+1}%slurp
%end for
; \\
-(TableName##_##Query *)getQuery; \\
-(TableName##_Cursor *)add; \\
-(TableName##_Cursor *)objectAtIndex:(size_t)ndx; \\
-(TableName##_Cursor *)back; \\
@end

#undef TDB_TABLE_${num_cols}
#define TDB_TABLE_${num_cols}(TableName%slurp
    %for $j in range($num_cols)
    , CType${j+1}, CName${j+1}%slurp
    %end for
    ) \\
TDB_TABLE_DEF_${num_cols}(TableName%slurp
    %for $j in range($num_cols)
    ,CType${j+1}, CName${j+1}%slurp
    %end for
    ) \\
TDB_TABLE_IMPL_${num_cols}(TableName%slurp
    %for $j in range($num_cols)
    ,CType${j+1}, CName${j+1}%slurp
    %end for
    )
    

%end for

"""

args = sys.argv[1:]
if len(args) != 1:
	sys.stderr.write("Please specify the maximum number of table columns\n")
	sys.exit(1)
max_cols = int(args[0])
t = Template(templateDef, searchList=[{'max_cols': max_cols}])
sys.stdout.write(str(t))