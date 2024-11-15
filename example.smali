###### Class com.github.javaparser.ast.Node (com.github.javaparser.ast.Node)
.class public abstract Lcom/github/javaparser/ast/Node;
.super Ljava/lang/Object;
.source "SourceFile"

# interfaces
.implements Ljava/lang/Cloneable;
.implements Lcom/github/javaparser/HasParentNode;
.implements Lcom/github/javaparser/ast/visitor/Visitable;
.implements Lcom/github/javaparser/ast/nodeTypes/NodeWithRange;
.implements Lcom/github/javaparser/ast/nodeTypes/NodeWithTokenRange;


# annotations
.annotation system Ldalvik/annotation/MemberClasses;
    value = {
        Lcom/github/javaparser/ast/Node$d;,
        Lcom/github/javaparser/ast/Node$e;,
        Lcom/github/javaparser/ast/Node$c;,
        Lcom/github/javaparser/ast/Node$b;,
        Lcom/github/javaparser/ast/Node$a;,
        Lcom/github/javaparser/ast/Node$TreeTraversal;,
        Lcom/github/javaparser/ast/Node$Parsedness;,
        Lcom/github/javaparser/ast/Node$ObserverRegistrationMode;
    }
.end annotation

.annotation system Ldalvik/annotation/Signature;
    value = {
        "Ljava/lang/Object;",
        "Ljava/lang/Cloneable;",
        "Lcom/github/javaparser/HasParentNode<",
        "Lcom/github/javaparser/ast/Node;",
        ">;",
        "Lcom/github/javaparser/ast/visitor/Visitable;",
        "Lcom/github/javaparser/ast/nodeTypes/NodeWithRange<",
        "Lcom/github/javaparser/ast/Node;",
        ">;",
        "Lcom/github/javaparser/ast/nodeTypes/NodeWithTokenRange<",
        "Lcom/github/javaparser/ast/Node;",
        ">;"
    }
.end annotation


# static fields
.field public static a:Ljava/util/Comparator;
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "Ljava/util/Comparator<",
            "Lcom/github/javaparser/ast/nodeTypes/NodeWithRange<",
            "*>;>;"
        }
    .end annotation
.end field

.field public static final b:LTD;

.field public static final c:Lcom/github/javaparser/printer/PrettyPrinterConfiguration;

.field public static final d:Lqt;
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "Lqt<",
            "Lcom/github/javaparser/resolution/SymbolResolver;",
            ">;"
        }
    .end annotation
.end field

.field static final MULTIPLE_BINDINGS_URL:Ljava/lang/String; = "http://www.slf4j.org/codes.html#multiple_bindings"

# instance fields
.field public e:LTs;

.field public f:L_s;

.field public g:Lcom/github/javaparser/ast/Node;

.field public h:Ljava/util/List;
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "Ljava/util/List<",
            "Lcom/github/javaparser/ast/Node;",
            ">;"
        }
    .end annotation
.end field

.field public i:Ljava/util/List;
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "Ljava/util/List<",
            "LQt;",
            ">;"
        }
    .end annotation
.end field

.field public j:Ljava/util/IdentityHashMap;
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "Ljava/util/IdentityHashMap<",
            "Lqt<",
            "*>;",
            "Ljava/lang/Object;",
            ">;"
        }
    .end annotation
.end field

.field public k:LQt;

.field public l:Ljava/util/List;
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "Ljava/util/List<",
            "Lcom/github/javaparser/ast/observer/AstObserver;",
            ">;"
        }
    .end annotation
.end field

.field public m:Lcom/github/javaparser/ast/Node$Parsedness;


# direct methods
.method static constructor <clinit>()V
    .registers 2

    .line 1
    sget-object v0, Let;->a:Let;

    sput-object v0, Lcom/github/javaparser/ast/Node;->a:Ljava/util/Comparator;

    .line 2
    new-instance v0, LTD;

    new-instance v1, Lcom/github/javaparser/printer/PrettyPrinterConfiguration;

    invoke-direct {v1}, Lcom/github/javaparser/printer/PrettyPrinterConfiguration;-><init>()V

    invoke-direct {v0, v1}, LTD;-><init>(Lcom/github/javaparser/printer/PrettyPrinterConfiguration;)V

    sput-object v0, Lcom/github/javaparser/ast/Node;->b:LTD;

    .line 3
    new-instance v0, Lcom/github/javaparser/printer/PrettyPrinterConfiguration;

    invoke-direct {v0}, Lcom/github/javaparser/printer/PrettyPrinterConfiguration;-><init>()V

    const/4 v1, 0x0

    invoke-virtual {v0, v1}, Lcom/github/javaparser/printer/PrettyPrinterConfiguration;->a(Z)Lcom/github/javaparser/printer/PrettyPrinterConfiguration;

    sput-object v0, Lcom/github/javaparser/ast/Node;->c:Lcom/github/javaparser/printer/PrettyPrinterConfiguration;

    .line 4
    new-instance v0, Lst;

    invoke-direct {v0}, Lst;-><init>()V

    sput-object v0, Lcom/github/javaparser/ast/Node;->d:Lqt;

    return-void
.end method

.method public constructor <init>(L_s;)V
    .registers 3

    .line 1
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    .line 2
    new-instance v0, Ljava/util/LinkedList;

    invoke-direct {v0}, Ljava/util/LinkedList;-><init>()V

    iput-object v0, p0, Lcom/github/javaparser/ast/Node;->h:Ljava/util/List;

    .line 3
    new-instance v0, Ljava/util/LinkedList;

    invoke-direct {v0}, Ljava/util/LinkedList;-><init>()V

    iput-object v0, p0, Lcom/github/javaparser/ast/Node;->i:Ljava/util/List;

    const/4 v0, 0x0

    .line 4
    iput-object v0, p0, Lcom/github/javaparser/ast/Node;->j:Ljava/util/IdentityHashMap;

    .line 5
    new-instance v0, Ljava/util/ArrayList;

    invoke-direct {v0}, Ljava/util/ArrayList;-><init>()V

    iput-object v0, p0, Lcom/github/javaparser/ast/Node;->l:Ljava/util/List;

    .line 6
    sget-object v0, Lcom/github/javaparser/ast/Node$Parsedness;->PARSED:Lcom/github/javaparser/ast/Node$Parsedness;

    iput-object v0, p0, Lcom/github/javaparser/ast/Node;->m:Lcom/github/javaparser/ast/Node$Parsedness;

    .line 7
    invoke-virtual {p0, p1}, Lcom/github/javaparser/ast/Node;->a(L_s;)Lcom/github/javaparser/ast/Node;

    return-void
.end method

.method public static synthetic a(Lcom/github/javaparser/ast/nodeTypes/NodeWithRange;Lcom/github/javaparser/ast/nodeTypes/NodeWithRange;)I
    .registers 3

    .line 2
    invoke-interface {p0}, Lcom/github/javaparser/ast/nodeTypes/NodeWithRange;->e()Ljava/util/Optional;

    move-result-object v0

    invoke-virtual {v0}, Ljava/util/Optional;->isPresent()Z

    move-result v0

    if-eqz v0, :cond_31

    invoke-interface {p1}, Lcom/github/javaparser/ast/nodeTypes/NodeWithRange;->e()Ljava/util/Optional;

    move-result-object v0

    invoke-virtual {v0}, Ljava/util/Optional;->isPresent()Z

    move-result v0

    if-eqz v0, :cond_31

    .line 3
    invoke-interface {p0}, Lcom/github/javaparser/ast/nodeTypes/NodeWithRange;->e()Ljava/util/Optional;

    move-result-object p0

    invoke-virtual {p0}, Ljava/util/Optional;->get()Ljava/lang/Object;

    move-result-object p0

    check-cast p0, LTs;

    iget-object p0, p0, LTs;->a:LQs;

    invoke-interface {p1}, Lcom/github/javaparser/ast/nodeTypes/NodeWithRange;->e()Ljava/util/Optional;

    move-result-object p1

    invoke-virtual {p1}, Ljava/util/Optional;->get()Ljava/lang/Object;

    move-result-object p1

    check-cast p1, LTs;

    iget-object p1, p1, LTs;->a:LQs;

    invoke-virtual {p0, p1}, LQs;->a(LQs;)I

    move-result p0

    return p0

    .line 4
    :cond_31
    invoke-interface {p0}, Lcom/github/javaparser/ast/nodeTypes/NodeWithRange;->e()Ljava/util/Optional;

    move-result-object v0

    invoke-virtual {v0}, Ljava/util/Optional;->isPresent()Z

    move-result v0

    if-nez v0, :cond_48

    invoke-interface {p1}, Lcom/github/javaparser/ast/nodeTypes/NodeWithRange;->e()Ljava/util/Optional;

    move-result-object p1

    invoke-virtual {p1}, Ljava/util/Optional;->isPresent()Z

    move-result p1

    if-eqz p1, :cond_46

    goto :goto_48

    :cond_46
    const/4 p0, 0x0

    return p0

    .line 5
    :cond_48
    :goto_48
    invoke-interface {p0}, Lcom/github/javaparser/ast/nodeTypes/NodeWithRange;->e()Ljava/util/Optional;

    move-result-object p0

    invoke-virtual {p0}, Ljava/util/Optional;->isPresent()Z

    move-result p0

    if-eqz p0, :cond_54

    const/4 p0, 0x1

    return p0

    :cond_54
    const/4 p0, -0x1

    return p0
.end method

.method public static synthetic a(Lcom/github/javaparser/ast/observer/AstObserver;Lcom/github/javaparser/ast/Node;)V
    .registers 2

    .line 35
    invoke-virtual {p1, p0}, Lcom/github/javaparser/ast/Node;->d(Lcom/github/javaparser/ast/observer/AstObserver;)V

    return-void
.end method

.method public static synthetic a(Ljava/lang/Class;Ljava/util/function/Consumer;Lcom/github/javaparser/ast/Node;)V
    .registers 4

    .line 43
    invoke-virtual {p2}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    move-result-object v0

    invoke-virtual {p0, v0}, Ljava/lang/Class;->isAssignableFrom(Ljava/lang/Class;)Z

    move-result v0

    if-eqz v0, :cond_11

    .line 44
    invoke-virtual {p0, p2}, Ljava/lang/Class;->cast(Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object p0

    invoke-interface {p1, p0}, Ljava/util/function/Consumer;->accept(Ljava/lang/Object;)V

    :cond_11
    return-void
.end method


# virtual methods
.method public a(LTs;)Lcom/github/javaparser/ast/Node;
    .registers 4

    .line 10
    iget-object v0, p0, Lcom/github/javaparser/ast/Node;->e:LTs;

    if-ne v0, p1, :cond_5

    return-object p0

    .line 11
    :cond_5
    sget-object v1, Lcom/github/javaparser/ast/observer/ObservableProperty;->RANGE:Lcom/github/javaparser/ast/observer/ObservableProperty;

    invoke-virtual {p0, v1, v0, p1}, Lcom/github/javaparser/ast/Node;->a(Lcom/github/javaparser/ast/observer/ObservableProperty;Ljava/lang/Object;Ljava/lang/Object;)V

    .line 12
    iput-object p1, p0, Lcom/github/javaparser/ast/Node;->e:LTs;

    return-object p0
.end method

.method public a(L_s;)Lcom/github/javaparser/ast/Node;
    .registers 4

    .line 6
    iput-object p1, p0, Lcom/github/javaparser/ast/Node;->f:L_s;

    if-eqz p1, :cond_49

    .line 7
    invoke-virtual {p1}, L_s;->a()Lcom/github/javaparser/JavaToken;

    move-result-object v0

    invoke-virtual {v0}, Lcom/github/javaparser/JavaToken;->e()Ljava/util/Optional;

    move-result-object v0

    invoke-virtual {v0}, Ljava/util/Optional;->isPresent()Z

    move-result v0

    if-eqz v0, :cond_49

    invoke-virtual {p1}, L_s;->a()Lcom/github/javaparser/JavaToken;

    move-result-object v0

    invoke-virtual {v0}, Lcom/github/javaparser/JavaToken;->e()Ljava/util/Optional;

    move-result-object v0

    invoke-virtual {v0}, Ljava/util/Optional;->isPresent()Z

    move-result v0

    if-nez v0, :cond_21

    goto :goto_49

    .line 8
    :cond_21
    new-instance v0, LTs;

    invoke-virtual {p1}, L_s;->a()Lcom/github/javaparser/JavaToken;

    move-result-object v1

    invoke-virtual {v1}, Lcom/github/javaparser/JavaToken;->e()Ljava/util/Optional;

    move-result-object v1

    invoke-virtual {v1}, Ljava/util/Optional;->get()Ljava/lang/Object;

    move-result-object v1

    check-cast v1, LTs;

    iget-object v1, v1, LTs;->a:LQs;

    invoke-virtual {p1}, L_s;->b()Lcom/github/javaparser/JavaToken;

    move-result-object p1

    invoke-virtual {p1}, Lcom/github/javaparser/JavaToken;->e()Ljava/util/Optional;

    move-result-object p1

    invoke-virtual {p1}, Ljava/util/Optional;->get()Ljava/lang/Object;

    move-result-object p1

    check-cast p1, LTs;

    iget-object p1, p1, LTs;->b:LQs;

    invoke-direct {v0, v1, p1}, LTs;-><init>(LQs;LQs;)V

    iput-object v0, p0, Lcom/github/javaparser/ast/Node;->e:LTs;

    goto :goto_4c

    :cond_49
    :goto_49
    const/4 p1, 0x0

    .line 9
    iput-object p1, p0, Lcom/github/javaparser/ast/Node;->e:LTs;

    :goto_4c
    return-object p0
.end method

.method public a(Lcom/github/javaparser/ast/Node$Parsedness;)Lcom/github/javaparser/ast/Node;
    .registers 2

    .line 36
    iput-object p1, p0, Lcom/github/javaparser/ast/Node;->m:Lcom/github/javaparser/ast/Node$Parsedness;

    return-object p0
.end method

.method public a(Lcom/github/javaparser/ast/Node;)Lcom/github/javaparser/ast/Node;
    .registers 5

    .line 15
    iget-object v0, p0, Lcom/github/javaparser/ast/Node;->g:Lcom/github/javaparser/ast/Node;

    if-ne p1, v0, :cond_5

    return-object p0

    .line 16
    :cond_5
    iget-object v0, p0, Lcom/github/javaparser/ast/Node;->l:Ljava/util/List;

    new-instance v1, Lgt;

    invoke-direct {v1, p0, p1}, Lgt;-><init>(Lcom/github/javaparser/ast/Node;Lcom/github/javaparser/ast/Node;)V

    invoke-interface {v0, v1}, Ljava/util/List;->forEach(Ljava/util/function/Consumer;)V

    .line 17
    iget-object v0, p0, Lcom/github/javaparser/ast/Node;->g:Lcom/github/javaparser/ast/Node;

    if-eqz v0, :cond_28

    .line 18
    iget-object v0, v0, Lcom/github/javaparser/ast/Node;->h:Ljava/util/List;

    const/4 v1, 0x0

    .line 19
    :goto_16
    invoke-interface {v0}, Ljava/util/List;->size()I

    move-result v2

    if-ge v1, v2, :cond_28

    .line 20
    invoke-interface {v0, v1}, Ljava/util/List;->get(I)Ljava/lang/Object;

    move-result-object v2

    if-ne v2, p0, :cond_25

    .line 21
    invoke-interface {v0, v1}, Ljava/util/List;->remove(I)Ljava/lang/Object;

    :cond_25
    add-int/lit8 v1, v1, 0x1

    goto :goto_16

    .line 22
    :cond_28
    iput-object p1, p0, Lcom/github/javaparser/ast/Node;->g:Lcom/github/javaparser/ast/Node;

    .line 23
    iget-object p1, p0, Lcom/github/javaparser/ast/Node;->g:Lcom/github/javaparser/ast/Node;

    if-eqz p1, :cond_33

    .line 24
    iget-object p1, p1, Lcom/github/javaparser/ast/Node;->h:Ljava/util/List;

    invoke-interface {p1, p0}, Ljava/util/List;->add(Ljava/lang/Object;)Z

    :cond_33
    return-object p0
.end method

.method public bridge synthetic a(Lcom/github/javaparser/ast/Node;)Ljava/lang/Object;
    .registers 2

    .line 1
    invoke-virtual {p0, p1}, Lcom/github/javaparser/ast/Node;->a(Lcom/github/javaparser/ast/Node;)Lcom/github/javaparser/ast/Node;

    return-object p0
.end method

.method public synthetic a(Lcom/github/javaparser/ast/Node$TreeTraversal;)Ljava/util/Iterator;
    .registers 2

    .line 39
    invoke-virtual {p0, p1}, Lcom/github/javaparser/ast/Node;->c(Lcom/github/javaparser/ast/Node$TreeTraversal;)Ljava/util/Iterator;

    move-result-object p1

    return-object p1
.end method

.method public synthetic a()Ljava/util/Optional;
    .registers 2
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "()",
            "Ljava/util/Optional<",
            "LQs;",
            ">;"
        }
    .end annotation

    invoke-static {p0}, LXu;->b(Lcom/github/javaparser/ast/nodeTypes/NodeWithRange;)Ljava/util/Optional;

    move-result-object v0

    return-object v0
.end method

.method public synthetic a(Ljava/lang/Class;)Ljava/util/Optional;
    .registers 2
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "<N:",
            "Ljava/lang/Object;",
            ">(",
            "Ljava/lang/Class<",
            "TN;>;)",
            "Ljava/util/Optional<",
            "TN;>;"
        }
    .end annotation

    invoke-static {p0, p1}, LMs;->a(Lcom/github/javaparser/HasParentNode;Ljava/lang/Class;)Ljava/util/Optional;

    move-result-object p1

    return-object p1
.end method

.method public a(LQt;)V
    .registers 3

    .line 13
    iget-object v0, p0, Lcom/github/javaparser/ast/Node;->i:Ljava/util/List;

    invoke-interface {v0, p1}, Ljava/util/List;->add(Ljava/lang/Object;)Z

    .line 14
    invoke-virtual {p1, p0}, Lcom/github/javaparser/ast/Node;->a(Lcom/github/javaparser/ast/Node;)Lcom/github/javaparser/ast/Node;

    return-void
.end method

.method public a(Lcom/github/javaparser/ast/Node$TreeTraversal;Ljava/util/function/Consumer;)V
    .registers 4
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "(",
            "Lcom/github/javaparser/ast/Node$TreeTraversal;",
            "Ljava/util/function/Consumer<",
            "Lcom/github/javaparser/ast/Node;",
            ">;)V"
        }
    .end annotation

    .line 40
    invoke-virtual {p0, p1}, Lcom/github/javaparser/ast/Node;->b(Lcom/github/javaparser/ast/Node$TreeTraversal;)Ljava/lang/Iterable;

    move-result-object p1

    invoke-interface {p1}, Ljava/lang/Iterable;->iterator()Ljava/util/Iterator;

    move-result-object p1

    :goto_8
    invoke-interface {p1}, Ljava/util/Iterator;->hasNext()Z

    move-result v0

    if-eqz v0, :cond_18

    invoke-interface {p1}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    move-result-object v0

    check-cast v0, Lcom/github/javaparser/ast/Node;

    .line 41
    invoke-interface {p2, v0}, Ljava/util/function/Consumer;->accept(Ljava/lang/Object;)V

    goto :goto_8

    :cond_18
    return-void
.end method

.method public synthetic a(Lcom/github/javaparser/ast/Node;Lcom/github/javaparser/ast/observer/AstObserver;)V
    .registers 4

    .line 25
    iget-object v0, p0, Lcom/github/javaparser/ast/Node;->g:Lcom/github/javaparser/ast/Node;

    invoke-interface {p2, p0, v0, p1}, Lcom/github/javaparser/ast/observer/AstObserver;->a(Lcom/github/javaparser/ast/Node;Lcom/github/javaparser/ast/Node;Lcom/github/javaparser/ast/Node;)V

    return-void
.end method

.method public a(Lcom/github/javaparser/ast/observer/AstObserver;)V
    .registers 3

    .line 34
    iget-object v0, p0, Lcom/github/javaparser/ast/Node;->l:Ljava/util/List;

    invoke-interface {v0, p1}, Ljava/util/List;->remove(Ljava/lang/Object;)Z

    return-void
.end method

.method public a(Lcom/github/javaparser/ast/observer/ObservableProperty;Ljava/lang/Object;Ljava/lang/Object;)V
    .registers 6
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "<P:",
            "Ljava/lang/Object;",
            ">(",
            "Lcom/github/javaparser/ast/observer/ObservableProperty;",
            "TP;TP;)V"
        }
    .end annotation

    .line 33
    iget-object v0, p0, Lcom/github/javaparser/ast/Node;->l:Ljava/util/List;

    new-instance v1, Lht;

    invoke-direct {v1, p0, p1, p2, p3}, Lht;-><init>(Lcom/github/javaparser/ast/Node;Lcom/github/javaparser/ast/observer/ObservableProperty;Ljava/lang/Object;Ljava/lang/Object;)V

    invoke-interface {v0, v1}, Ljava/util/List;->forEach(Ljava/util/function/Consumer;)V

    return-void
.end method

.method public synthetic a(Lcom/github/javaparser/ast/observer/ObservableProperty;Ljava/lang/Object;Ljava/lang/Object;Lcom/github/javaparser/ast/observer/AstObserver;)V
    .registers 5

    .line 32
    invoke-interface {p4, p0, p1, p2, p3}, Lcom/github/javaparser/ast/observer/AstObserver;->a(Lcom/github/javaparser/ast/Node;Lcom/github/javaparser/ast/observer/ObservableProperty;Ljava/lang/Object;Ljava/lang/Object;)V

    return-void
.end method

.method public a(Ljava/lang/Class;Ljava/util/function/Consumer;)V
    .registers 5
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "<T:",
            "Lcom/github/javaparser/ast/Node;",
            ">(",
            "Ljava/lang/Class<",
            "TT;>;",
            "Ljava/util/function/Consumer<",
            "TT;>;)V"
        }
    .end annotation

    .line 42
    sget-object v0, Lcom/github/javaparser/ast/Node$TreeTraversal;->PREORDER:Lcom/github/javaparser/ast/Node$TreeTraversal;

    new-instance v1, Lct;

    invoke-direct {v1, p1, p2}, Lct;-><init>(Ljava/lang/Class;Ljava/util/function/Consumer;)V

    invoke-virtual {p0, v0, v1}, Lcom/github/javaparser/ast/Node;->a(Lcom/github/javaparser/ast/Node$TreeTraversal;Ljava/util/function/Consumer;)V

    return-void
.end method

.method public a(Lqt;Ljava/lang/Object;)V
    .registers 4
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "<M:",
            "Ljava/lang/Object;",
            ">(",
            "Lqt<",
            "TM;>;TM;)V"
        }
    .end annotation

    .line 26
    iget-object v0, p0, Lcom/github/javaparser/ast/Node;->j:Ljava/util/IdentityHashMap;

    if-nez v0, :cond_b

    .line 27
    new-instance v0, Ljava/util/IdentityHashMap;

    invoke-direct {v0}, Ljava/util/IdentityHashMap;-><init>()V

    iput-object v0, p0, Lcom/github/javaparser/ast/Node;->j:Ljava/util/IdentityHashMap;

    .line 28
    :cond_b
    iget-object v0, p0, Lcom/github/javaparser/ast/Node;->j:Ljava/util/IdentityHashMap;

    invoke-virtual {v0, p1, p2}, Ljava/util/IdentityHashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;

    return-void
.end method

.method public a(Lut;)V
    .registers 2
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "(",
            "Lut<",
            "+",
            "Lcom/github/javaparser/ast/Node;",
            ">;)V"
        }
    .end annotation

    if-eqz p1, :cond_8

    .line 31
    invoke-virtual {p0}, Lcom/github/javaparser/ast/Node;->v()Lcom/github/javaparser/ast/Node;

    invoke-virtual {p1, p0}, Lut;->a(Lcom/github/javaparser/ast/Node;)Lut;

    :cond_8
    return-void
.end method

.method public a(Lcom/github/javaparser/ast/Node;Lcom/github/javaparser/ast/Node;)Z
    .registers 5

    const/4 v0, 0x0

    if-nez p1, :cond_4

    return v0

    .line 37
    :cond_4
    iget-object v1, p0, Lcom/github/javaparser/ast/Node;->k:LQt;

    if-eqz v1, :cond_11

    if-ne p1, v1, :cond_11

    .line 38
    check-cast p2, LQt;

    invoke-virtual {p0, p2}, Lcom/github/javaparser/ast/Node;->b(LQt;)Lcom/github/javaparser/ast/Node;

    const/4 p1, 0x1

    return p1

    :cond_11
    return v0
.end method

.method public a(Lqt;)Z
    .registers 4
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "(",
            "Lqt<",
            "*>;)Z"
        }
    .end annotation

    .line 29
    iget-object v0, p0, Lcom/github/javaparser/ast/Node;->j:Ljava/util/IdentityHashMap;

    const/4 v1, 0x0

    if-nez v0, :cond_6

    return v1

    .line 30
    :cond_6
    invoke-virtual {v0, p1}, Ljava/util/IdentityHashMap;->get(Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object p1

    if-eqz p1, :cond_d

    const/4 v1, 0x1

    :cond_d
    return v1
.end method

.method public final b(LQt;)Lcom/github/javaparser/ast/Node;
    .registers 4

    .line 1
    iget-object v0, p0, Lcom/github/javaparser/ast/Node;->k:LQt;

    if-ne v0, p1, :cond_5

    return-object p0

    :cond_5
    if-eqz p1, :cond_14

    .line 2
    instance-of v0, p0, LQt;

    if-nez v0, :cond_c

    goto :goto_14

    .line 3
    :cond_c
    new-instance p1, Ljava/lang/RuntimeException;

    const-string v0, "A comment can not be commented"

    invoke-direct {p1, v0}, Ljava/lang/RuntimeException;-><init>(Ljava/lang/String;)V

    throw p1

    .line 4
    :cond_14
    :goto_14
    sget-object v0, Lcom/github/javaparser/ast/observer/ObservableProperty;->COMMENT:Lcom/github/javaparser/ast/observer/ObservableProperty;

    iget-object v1, p0, Lcom/github/javaparser/ast/Node;->k:LQt;

    invoke-virtual {p0, v0, v1, p1}, Lcom/github/javaparser/ast/Node;->a(Lcom/github/javaparser/ast/observer/ObservableProperty;Ljava/lang/Object;Ljava/lang/Object;)V

    .line 5
    iget-object v0, p0, Lcom/github/javaparser/ast/Node;->k:LQt;

    if-eqz v0, :cond_23

    const/4 v1, 0x0

    .line 6
    invoke-virtual {v0, v1}, LQt;->e(Lcom/github/javaparser/ast/Node;)LQt;

    .line 7
    :cond_23
    iput-object p1, p0, Lcom/github/javaparser/ast/Node;->k:LQt;

    if-eqz p1, :cond_2c

    .line 8
    iget-object p1, p0, Lcom/github/javaparser/ast/Node;->k:LQt;

    invoke-virtual {p1, p0}, LQt;->e(Lcom/github/javaparser/ast/Node;)LQt;

    :cond_2c
    return-object p0
.end method

.method public final b(Lcom/github/javaparser/ast/Node$TreeTraversal;)Ljava/lang/Iterable;
    .registers 3
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "(",
            "Lcom/github/javaparser/ast/Node$TreeTraversal;",
            ")",
            "Ljava/lang/Iterable<",
            "Lcom/github/javaparser/ast/Node;",
            ">;"
        }
    .end annotation

    .line 12
    new-instance v0, Ldt;

    invoke-direct {v0, p0, p1}, Ldt;-><init>(Lcom/github/javaparser/ast/Node;Lcom/github/javaparser/ast/Node$TreeTraversal;)V

    return-object v0
.end method

.method public b(Lqt;)Ljava/lang/Object;
    .registers 3
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "<M:",
            "Ljava/lang/Object;",
            ">(",
            "Lqt<",
            "TM;>;)TM;"
        }
    .end annotation

    .line 9
    iget-object v0, p0, Lcom/github/javaparser/ast/Node;->j:Ljava/util/IdentityHashMap;

    if-nez v0, :cond_6

    const/4 p1, 0x0

    return-object p1

    .line 10
    :cond_6
    invoke-virtual {v0, p1}, Ljava/util/IdentityHashMap;->get(Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object p1

    return-object p1
.end method

.method public b(Ljava/lang/Class;)Ljava/util/List;
    .registers 4
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "<T:",
            "Lcom/github/javaparser/ast/Node;",
            ">(",
            "Ljava/lang/Class<",
            "TT;>;)",
            "Ljava/util/List<",
            "TT;>;"
        }
    .end annotation

    .line 13
    new-instance v0, Ljava/util/ArrayList;

    invoke-direct {v0}, Ljava/util/ArrayList;-><init>()V

    .line 14
    invoke-virtual {v0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    new-instance v1, Lmt;

    invoke-direct {v1, v0}, Lmt;-><init>(Ljava/util/List;)V

    invoke-virtual {p0, p1, v1}, Lcom/github/javaparser/ast/Node;->a(Ljava/lang/Class;Ljava/util/function/Consumer;)V

    return-object v0
.end method

.method public synthetic b(Lcom/github/javaparser/ast/Node;)Z
    .registers 2

    invoke-static {p0, p1}, LXu;->a(Lcom/github/javaparser/ast/nodeTypes/NodeWithRange;Lcom/github/javaparser/ast/Node;)Z

    move-result p1

    return p1
.end method

.method public b(Lcom/github/javaparser/ast/observer/AstObserver;)Z
    .registers 3

    .line 11
    iget-object v0, p0, Lcom/github/javaparser/ast/Node;->l:Ljava/util/List;

    invoke-interface {v0, p1}, Ljava/util/List;->contains(Ljava/lang/Object;)Z

    move-result p1

    return p1
.end method

.method public final c(Lcom/github/javaparser/ast/Node$TreeTraversal;)Ljava/util/Iterator;
    .registers 3
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "(",
            "Lcom/github/javaparser/ast/Node$TreeTraversal;",
            ")",
            "Ljava/util/Iterator<",
            "Lcom/github/javaparser/ast/Node;",
            ">;"
        }
    .end annotation

    .line 4
    sget-object v0, Ltt;->b:[I

    invoke-virtual {p1}, Ljava/lang/Enum;->ordinal()I

    move-result p1

    aget p1, v0, p1

    const/4 v0, 0x1

    if-eq p1, v0, :cond_37

    const/4 v0, 0x2

    if-eq p1, v0, :cond_31

    const/4 v0, 0x3

    if-eq p1, v0, :cond_2b

    const/4 v0, 0x4

    if-eq p1, v0, :cond_25

    const/4 v0, 0x5

    if-ne p1, v0, :cond_1d

    .line 5
    new-instance p1, Lcom/github/javaparser/ast/Node$c;

    invoke-direct {p1, p0}, Lcom/github/javaparser/ast/Node$c;-><init>(Lcom/github/javaparser/ast/Node;)V

    return-object p1

    .line 6
    :cond_1d
    new-instance p1, Ljava/lang/IllegalArgumentException;

    const-string v0, "Unknown traversal choice."

    invoke-direct {p1, v0}, Ljava/lang/IllegalArgumentException;-><init>(Ljava/lang/String;)V

    throw p1

    .line 7
    :cond_25
    new-instance p1, Lcom/github/javaparser/ast/Node$b;

    invoke-direct {p1, p0}, Lcom/github/javaparser/ast/Node$b;-><init>(Lcom/github/javaparser/ast/Node;)V

    return-object p1

    .line 8
    :cond_2b
    new-instance p1, Lcom/github/javaparser/ast/Node$e;

    invoke-direct {p1, p0}, Lcom/github/javaparser/ast/Node$e;-><init>(Lcom/github/javaparser/ast/Node;)V

    return-object p1

    .line 9
    :cond_31
    new-instance p1, Lcom/github/javaparser/ast/Node$d;

    invoke-direct {p1, p0}, Lcom/github/javaparser/ast/Node$d;-><init>(Lcom/github/javaparser/ast/Node;)V

    return-object p1

    .line 10
    :cond_37
    new-instance p1, Lcom/github/javaparser/ast/Node$a;

    invoke-direct {p1, p0}, Lcom/github/javaparser/ast/Node$a;-><init>(Lcom/github/javaparser/ast/Node;)V

    return-object p1
.end method

.method public c(Ljava/lang/Class;)Ljava/util/Optional;
    .registers 4
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "<N:",
            "Lcom/github/javaparser/ast/Node;",
            ">(",
            "Ljava/lang/Class<",
            "TN;>;)",
            "Ljava/util/Optional<",
            "TN;>;"
        }
    .end annotation

    move-object v0, p0

    .line 11
    :cond_1
    invoke-virtual {v0}, Lcom/github/javaparser/ast/Node;->getParentNode()Ljava/util/Optional;

    move-result-object v1

    invoke-virtual {v1}, Ljava/util/Optional;->isPresent()Z

    move-result v1

    if-eqz v1, :cond_28

    .line 12
    invoke-virtual {v0}, Lcom/github/javaparser/ast/Node;->getParentNode()Ljava/util/Optional;

    move-result-object v0

    invoke-virtual {v0}, Ljava/util/Optional;->get()Ljava/lang/Object;

    move-result-object v0

    check-cast v0, Lcom/github/javaparser/ast/Node;

    .line 13
    invoke-virtual {v0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    move-result-object v1

    invoke-virtual {p1, v1}, Ljava/lang/Class;->isAssignableFrom(Ljava/lang/Class;)Z

    move-result v1

    if-eqz v1, :cond_1

    .line 14
    invoke-virtual {p1, v0}, Ljava/lang/Class;->cast(Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object p1

    invoke-static {p1}, Ljava/util/Optional;->of(Ljava/lang/Object;)Ljava/util/Optional;

    move-result-object p1

    return-object p1

    .line 15
    :cond_28
    invoke-static {}, Ljava/util/Optional;->empty()Ljava/util/Optional;

    move-result-object p1

    return-object p1
.end method

.method public c(Lcom/github/javaparser/ast/observer/AstObserver;)V
    .registers 3

    .line 3
    iget-object v0, p0, Lcom/github/javaparser/ast/Node;->l:Ljava/util/List;

    invoke-interface {v0, p1}, Ljava/util/List;->add(Ljava/lang/Object;)Z

    return-void
.end method

.method public c(Lcom/github/javaparser/ast/Node;)Z
    .registers 3

    .line 1
    iget-object v0, p0, Lcom/github/javaparser/ast/Node;->g:Lcom/github/javaparser/ast/Node;

    if-nez v0, :cond_6

    const/4 p1, 0x0

    return p1

    .line 2
    :cond_6
    invoke-virtual {v0, p0, p1}, Lcom/github/javaparser/ast/Node;->a(Lcom/github/javaparser/ast/Node;Lcom/github/javaparser/ast/Node;)Z

    move-result p1

    return p1
.end method

.method public clone()Lcom/github/javaparser/ast/Node;
    .registers 3

    .line 2
    new-instance v0, LdB;

    invoke-direct {v0}, LdB;-><init>()V

    const/4 v1, 0x0

    invoke-interface {p0, v0, v1}, Lcom/github/javaparser/ast/visitor/Visitable;->a(Lcom/github/javaparser/ast/visitor/GenericVisitor;Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, Lcom/github/javaparser/ast/Node;

    return-object v0
.end method

.method public bridge synthetic clone()Ljava/lang/Object;
    .registers 2

    .line 1
    invoke-virtual {p0}, Lcom/github/javaparser/ast/Node;->clone()Lcom/github/javaparser/ast/Node;

    move-result-object v0

    return-object v0
.end method

.method public d(Lcom/github/javaparser/ast/Node;)V
    .registers 2

    if-eqz p1, :cond_8

    .line 1
    invoke-virtual {p0}, Lcom/github/javaparser/ast/Node;->v()Lcom/github/javaparser/ast/Node;

    invoke-virtual {p1, p0}, Lcom/github/javaparser/ast/Node;->a(Lcom/github/javaparser/ast/Node;)Lcom/github/javaparser/ast/Node;

    :cond_8
    return-void
.end method

.method public d(Lcom/github/javaparser/ast/observer/AstObserver;)V
    .registers 5

    .line 2
    invoke-virtual {p0, p1}, Lcom/github/javaparser/ast/Node;->c(Lcom/github/javaparser/ast/observer/AstObserver;)V

    .line 3
    invoke-virtual {p0}, Lcom/github/javaparser/ast/Node;->r()Ljava/util/List;

    move-result-object v0

    new-instance v1, Lft;

    invoke-direct {v1, p1}, Lft;-><init>(Lcom/github/javaparser/ast/observer/AstObserver;)V

    invoke-interface {v0, v1}, Ljava/util/List;->forEach(Ljava/util/function/Consumer;)V

    .line 4
    invoke-virtual {p0}, Lcom/github/javaparser/ast/Node;->t()LGC;

    move-result-object v0

    invoke-virtual {v0}, LyB;->a()Ljava/util/List;

    move-result-object v0

    invoke-interface {v0}, Ljava/util/List;->iterator()Ljava/util/Iterator;

    move-result-object v0

    :cond_1b
    :goto_1b
    invoke-interface {v0}, Ljava/util/Iterator;->hasNext()Z

    move-result v1

    if-eqz v1, :cond_39

    invoke-interface {v0}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    move-result-object v1

    check-cast v1, LNC;

    .line 5
    invoke-virtual {v1}, LNC;->c()Z

    move-result v2

    if-eqz v2, :cond_1b

    .line 6
    invoke-virtual {v1, p0}, LNC;->a(Lcom/github/javaparser/ast/Node;)Ljava/lang/Object;

    move-result-object v1

    check-cast v1, Lut;

    if-eqz v1, :cond_1b

    .line 7
    invoke-virtual {v1, p1}, Lut;->c(Lcom/github/javaparser/ast/observer/AstObserver;)V

    goto :goto_1b

    :cond_39
    return-void
.end method

.method public e()Ljava/util/Optional;
    .registers 2
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "()",
            "Ljava/util/Optional<",
            "LTs;",
            ">;"
        }
    .end annotation

    .line 1
    iget-object v0, p0, Lcom/github/javaparser/ast/Node;->e:LTs;

    invoke-static {v0}, Ljava/util/Optional;->ofNullable(Ljava/lang/Object;)Ljava/util/Optional;

    move-result-object v0

    return-object v0
.end method

.method public equals(Ljava/lang/Object;)Z
    .registers 3

    if-eqz p1, :cond_e

    .line 1
    instance-of v0, p1, Lcom/github/javaparser/ast/Node;

    if-nez v0, :cond_7

    goto :goto_e

    .line 2
    :cond_7
    check-cast p1, Lcom/github/javaparser/ast/Node;

    invoke-static {p0, p1}, LeB;->b(Lcom/github/javaparser/ast/Node;Lcom/github/javaparser/ast/Node;)Z

    move-result p1

    return p1

    :cond_e
    :goto_e
    const/4 p1, 0x0

    return p1
.end method

.method public getParentNode()Ljava/util/Optional;
    .registers 2
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "()",
            "Ljava/util/Optional<",
            "Lcom/github/javaparser/ast/Node;",
            ">;"
        }
    .end annotation

    .line 1
    iget-object v0, p0, Lcom/github/javaparser/ast/Node;->g:Lcom/github/javaparser/ast/Node;

    invoke-static {v0}, Ljava/util/Optional;->ofNullable(Ljava/lang/Object;)Ljava/util/Optional;

    move-result-object v0

    return-object v0
.end method

.method public final hashCode()I
    .registers 2

    .line 1
    invoke-static {p0}, LfB;->a(Lcom/github/javaparser/ast/Node;)I

    move-result v0

    return v0
.end method

.method public synthetic i()Ljava/util/Optional;
    .registers 2
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "()",
            "Ljava/util/Optional<",
            "LQs;",
            ">;"
        }
    .end annotation

    invoke-static {p0}, LXu;->a(Lcom/github/javaparser/ast/nodeTypes/NodeWithRange;)Ljava/util/Optional;

    move-result-object v0

    return-object v0
.end method

.method public p()Ljava/util/Optional;
    .registers 2
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "()",
            "Ljava/util/Optional<",
            "L_s;",
            ">;"
        }
    .end annotation

    .line 1
    iget-object v0, p0, Lcom/github/javaparser/ast/Node;->f:L_s;

    invoke-static {v0}, Ljava/util/Optional;->ofNullable(Ljava/lang/Object;)Ljava/util/Optional;

    move-result-object v0

    return-object v0
.end method

.method public q()V
    .registers 1

    return-void
.end method

.method public r()Ljava/util/List;
    .registers 2
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "()",
            "Ljava/util/List<",
            "Lcom/github/javaparser/ast/Node;",
            ">;"
        }
    .end annotation

    .line 1
    iget-object v0, p0, Lcom/github/javaparser/ast/Node;->h:Ljava/util/List;

    invoke-static {v0}, Ljava/util/Collections;->unmodifiableList(Ljava/util/List;)Ljava/util/List;

    move-result-object v0

    return-object v0
.end method

.method public s()Ljava/util/Optional;
    .registers 2
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "()",
            "Ljava/util/Optional<",
            "LQt;",
            ">;"
        }
    .end annotation

    .line 1
    iget-object v0, p0, Lcom/github/javaparser/ast/Node;->k:LQt;

    invoke-static {v0}, Ljava/util/Optional;->ofNullable(Ljava/lang/Object;)Ljava/util/Optional;

    move-result-object v0

    return-object v0
.end method

.method public t()LGC;
    .registers 2

    .line 1
    sget-object v0, LjC;->b:LGC;

    return-object v0
.end method

.method public final toString()Ljava/lang/String;
    .registers 2

    .line 1
    sget-object v0, Lcom/github/javaparser/ast/Node;->b:LTD;

    invoke-virtual {v0, p0}, LTD;->a(Lcom/github/javaparser/ast/Node;)Ljava/lang/String;

    move-result-object v0

    return-object v0
.end method

.method public u()Ljava/util/List;
    .registers 3
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "()",
            "Ljava/util/List<",
            "LQt;",
            ">;"
        }
    .end annotation

    .line 1
    new-instance v0, Ljava/util/LinkedList;

    iget-object v1, p0, Lcom/github/javaparser/ast/Node;->i:Ljava/util/List;

    invoke-direct {v0, v1}, Ljava/util/LinkedList;-><init>(Ljava/util/Collection;)V

    return-object v0
.end method

.method public v()Lcom/github/javaparser/ast/Node;
    .registers 1

    return-object p0
.end method

.method public w()Lcom/github/javaparser/ast/Node$Parsedness;
    .registers 2

    .line 1
    iget-object v0, p0, Lcom/github/javaparser/ast/Node;->m:Lcom/github/javaparser/ast/Node$Parsedness;

    return-object v0
.end method

###### Class com.github.javaparser.ast.Node.ObserverRegistrationMode (com.github.javaparser.ast.Node$ObserverRegistrationMode)
.class public final enum Lcom/github/javaparser/ast/Node$ObserverRegistrationMode;
.super Ljava/lang/Enum;
.source "SourceFile"


# annotations
.annotation system Ldalvik/annotation/EnclosingClass;
    value = Lcom/github/javaparser/ast/Node;
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x4019
    name = "ObserverRegistrationMode"
.end annotation

.annotation system Ldalvik/annotation/Signature;
    value = {
        "Ljava/lang/Enum<",
        "Lcom/github/javaparser/ast/Node$ObserverRegistrationMode;",
        ">;"
    }
.end annotation


# static fields
.field public static final enum JUST_THIS_NODE:Lcom/github/javaparser/ast/Node$ObserverRegistrationMode;

.field public static final enum SELF_PROPAGATING:Lcom/github/javaparser/ast/Node$ObserverRegistrationMode;

.field public static final enum THIS_NODE_AND_EXISTING_DESCENDANTS:Lcom/github/javaparser/ast/Node$ObserverRegistrationMode;

.field public static final synthetic a:[Lcom/github/javaparser/ast/Node$ObserverRegistrationMode;


# direct methods
.method static constructor <clinit>()V
    .registers 5

    .line 1
    new-instance v0, Lcom/github/javaparser/ast/Node$ObserverRegistrationMode;

    const/4 v1, 0x0

    const-string v2, "JUST_THIS_NODE"

    invoke-direct {v0, v2, v1}, Lcom/github/javaparser/ast/Node$ObserverRegistrationMode;-><init>(Ljava/lang/String;I)V

    sput-object v0, Lcom/github/javaparser/ast/Node$ObserverRegistrationMode;->JUST_THIS_NODE:Lcom/github/javaparser/ast/Node$ObserverRegistrationMode;

    .line 2
    new-instance v0, Lcom/github/javaparser/ast/Node$ObserverRegistrationMode;

    const/4 v2, 0x1

    const-string v3, "THIS_NODE_AND_EXISTING_DESCENDANTS"

    invoke-direct {v0, v3, v2}, Lcom/github/javaparser/ast/Node$ObserverRegistrationMode;-><init>(Ljava/lang/String;I)V

    sput-object v0, Lcom/github/javaparser/ast/Node$ObserverRegistrationMode;->THIS_NODE_AND_EXISTING_DESCENDANTS:Lcom/github/javaparser/ast/Node$ObserverRegistrationMode;

    .line 3
    new-instance v0, Lcom/github/javaparser/ast/Node$ObserverRegistrationMode;

    const/4 v3, 0x2

    const-string v4, "SELF_PROPAGATING"

    invoke-direct {v0, v4, v3}, Lcom/github/javaparser/ast/Node$ObserverRegistrationMode;-><init>(Ljava/lang/String;I)V

    sput-object v0, Lcom/github/javaparser/ast/Node$ObserverRegistrationMode;->SELF_PROPAGATING:Lcom/github/javaparser/ast/Node$ObserverRegistrationMode;

    const/4 v0, 0x3

    .line 4
    new-array v0, v0, [Lcom/github/javaparser/ast/Node$ObserverRegistrationMode;

    sget-object v4, Lcom/github/javaparser/ast/Node$ObserverRegistrationMode;->JUST_THIS_NODE:Lcom/github/javaparser/ast/Node$ObserverRegistrationMode;

    aput-object v4, v0, v1

    sget-object v1, Lcom/github/javaparser/ast/Node$ObserverRegistrationMode;->THIS_NODE_AND_EXISTING_DESCENDANTS:Lcom/github/javaparser/ast/Node$ObserverRegistrationMode;

    aput-object v1, v0, v2

    sget-object v1, Lcom/github/javaparser/ast/Node$ObserverRegistrationMode;->SELF_PROPAGATING:Lcom/github/javaparser/ast/Node$ObserverRegistrationMode;

    aput-object v1, v0, v3

    sput-object v0, Lcom/github/javaparser/ast/Node$ObserverRegistrationMode;->a:[Lcom/github/javaparser/ast/Node$ObserverRegistrationMode;

    return-void
.end method

.method public constructor <init>(Ljava/lang/String;I)V
    .registers 3
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "()V"
        }
    .end annotation

    .line 1
    invoke-direct {p0, p1, p2}, Ljava/lang/Enum;-><init>(Ljava/lang/String;I)V

    return-void
.end method

.method public static valueOf(Ljava/lang/String;)Lcom/github/javaparser/ast/Node$ObserverRegistrationMode;
    .registers 2

    .line 1
    const-class v0, Lcom/github/javaparser/ast/Node$ObserverRegistrationMode;

    invoke-static {v0, p0}, Ljava/lang/Enum;->valueOf(Ljava/lang/Class;Ljava/lang/String;)Ljava/lang/Enum;

    move-result-object p0

    check-cast p0, Lcom/github/javaparser/ast/Node$ObserverRegistrationMode;

    return-object p0
.end method

.method public static values()[Lcom/github/javaparser/ast/Node$ObserverRegistrationMode;
    .registers 1

    .line 1
    sget-object v0, Lcom/github/javaparser/ast/Node$ObserverRegistrationMode;->a:[Lcom/github/javaparser/ast/Node$ObserverRegistrationMode;

    invoke-virtual {v0}, [Lcom/github/javaparser/ast/Node$ObserverRegistrationMode;->clone()Ljava/lang/Object;

    move-result-object v0

    check-cast v0, [Lcom/github/javaparser/ast/Node$ObserverRegistrationMode;

    return-object v0
.end method

###### Class com.github.javaparser.ast.Node.Parsedness (com.github.javaparser.ast.Node$Parsedness)
.class public final enum Lcom/github/javaparser/ast/Node$Parsedness;
.super Ljava/lang/Enum;
.source "SourceFile"


# annotations
.annotation system Ldalvik/annotation/EnclosingClass;
    value = Lcom/github/javaparser/ast/Node;
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x4019
    name = "Parsedness"
.end annotation

.annotation system Ldalvik/annotation/Signature;
    value = {
        "Ljava/lang/Enum<",
        "Lcom/github/javaparser/ast/Node$Parsedness;",
        ">;"
    }
.end annotation


# static fields
.field public static final enum PARSED:Lcom/github/javaparser/ast/Node$Parsedness;

.field public static final enum UNPARSABLE:Lcom/github/javaparser/ast/Node$Parsedness;

.field public static final synthetic a:[Lcom/github/javaparser/ast/Node$Parsedness;


# direct methods
.method static constructor <clinit>()V
    .registers 4

    .line 1
    new-instance v0, Lcom/github/javaparser/ast/Node$Parsedness;

    const/4 v1, 0x0

    const-string v2, "PARSED"

    invoke-direct {v0, v2, v1}, Lcom/github/javaparser/ast/Node$Parsedness;-><init>(Ljava/lang/String;I)V

    sput-object v0, Lcom/github/javaparser/ast/Node$Parsedness;->PARSED:Lcom/github/javaparser/ast/Node$Parsedness;

    new-instance v0, Lcom/github/javaparser/ast/Node$Parsedness;

    const/4 v2, 0x1

    const-string v3, "UNPARSABLE"

    invoke-direct {v0, v3, v2}, Lcom/github/javaparser/ast/Node$Parsedness;-><init>(Ljava/lang/String;I)V

    sput-object v0, Lcom/github/javaparser/ast/Node$Parsedness;->UNPARSABLE:Lcom/github/javaparser/ast/Node$Parsedness;

    const/4 v0, 0x2

    .line 2
    new-array v0, v0, [Lcom/github/javaparser/ast/Node$Parsedness;

    sget-object v3, Lcom/github/javaparser/ast/Node$Parsedness;->PARSED:Lcom/github/javaparser/ast/Node$Parsedness;

    aput-object v3, v0, v1

    sget-object v1, Lcom/github/javaparser/ast/Node$Parsedness;->UNPARSABLE:Lcom/github/javaparser/ast/Node$Parsedness;

    aput-object v1, v0, v2

    sput-object v0, Lcom/github/javaparser/ast/Node$Parsedness;->a:[Lcom/github/javaparser/ast/Node$Parsedness;

    return-void
.end method

.method public constructor <init>(Ljava/lang/String;I)V
    .registers 3
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "()V"
        }
    .end annotation

    .line 1
    invoke-direct {p0, p1, p2}, Ljava/lang/Enum;-><init>(Ljava/lang/String;I)V

    return-void
.end method

.method public static valueOf(Ljava/lang/String;)Lcom/github/javaparser/ast/Node$Parsedness;
    .registers 2

    .line 1
    const-class v0, Lcom/github/javaparser/ast/Node$Parsedness;

    invoke-static {v0, p0}, Ljava/lang/Enum;->valueOf(Ljava/lang/Class;Ljava/lang/String;)Ljava/lang/Enum;

    move-result-object p0

    check-cast p0, Lcom/github/javaparser/ast/Node$Parsedness;

    return-object p0
.end method

.method public static values()[Lcom/github/javaparser/ast/Node$Parsedness;
    .registers 1

    .line 1
    sget-object v0, Lcom/github/javaparser/ast/Node$Parsedness;->a:[Lcom/github/javaparser/ast/Node$Parsedness;

    invoke-virtual {v0}, [Lcom/github/javaparser/ast/Node$Parsedness;->clone()Ljava/lang/Object;

    move-result-object v0

    check-cast v0, [Lcom/github/javaparser/ast/Node$Parsedness;

    return-object v0
.end method

###### Class com.github.javaparser.ast.Node.TreeTraversal (com.github.javaparser.ast.Node$TreeTraversal)
.class public final enum Lcom/github/javaparser/ast/Node$TreeTraversal;
.super Ljava/lang/Enum;
.source "SourceFile"


# annotations
.annotation system Ldalvik/annotation/EnclosingClass;
    value = Lcom/github/javaparser/ast/Node;
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x4019
    name = "TreeTraversal"
.end annotation

.annotation system Ldalvik/annotation/Signature;
    value = {
        "Ljava/lang/Enum<",
        "Lcom/github/javaparser/ast/Node$TreeTraversal;",
        ">;"
    }
.end annotation


# static fields
.field public static final enum BREADTHFIRST:Lcom/github/javaparser/ast/Node$TreeTraversal;

.field public static final enum DIRECT_CHILDREN:Lcom/github/javaparser/ast/Node$TreeTraversal;

.field public static final enum PARENTS:Lcom/github/javaparser/ast/Node$TreeTraversal;

.field public static final enum POSTORDER:Lcom/github/javaparser/ast/Node$TreeTraversal;

.field public static final enum PREORDER:Lcom/github/javaparser/ast/Node$TreeTraversal;

.field public static final synthetic a:[Lcom/github/javaparser/ast/Node$TreeTraversal;


# direct methods
.method static constructor <clinit>()V
    .registers 7

    .line 1
    new-instance v0, Lcom/github/javaparser/ast/Node$TreeTraversal;

    const/4 v1, 0x0

    const-string v2, "PREORDER"

    invoke-direct {v0, v2, v1}, Lcom/github/javaparser/ast/Node$TreeTraversal;-><init>(Ljava/lang/String;I)V

    sput-object v0, Lcom/github/javaparser/ast/Node$TreeTraversal;->PREORDER:Lcom/github/javaparser/ast/Node$TreeTraversal;

    new-instance v0, Lcom/github/javaparser/ast/Node$TreeTraversal;

    const/4 v2, 0x1

    const-string v3, "BREADTHFIRST"

    invoke-direct {v0, v3, v2}, Lcom/github/javaparser/ast/Node$TreeTraversal;-><init>(Ljava/lang/String;I)V

    sput-object v0, Lcom/github/javaparser/ast/Node$TreeTraversal;->BREADTHFIRST:Lcom/github/javaparser/ast/Node$TreeTraversal;

    new-instance v0, Lcom/github/javaparser/ast/Node$TreeTraversal;

    const/4 v3, 0x2

    const-string v4, "POSTORDER"

    invoke-direct {v0, v4, v3}, Lcom/github/javaparser/ast/Node$TreeTraversal;-><init>(Ljava/lang/String;I)V

    sput-object v0, Lcom/github/javaparser/ast/Node$TreeTraversal;->POSTORDER:Lcom/github/javaparser/ast/Node$TreeTraversal;

    new-instance v0, Lcom/github/javaparser/ast/Node$TreeTraversal;

    const/4 v4, 0x3

    const-string v5, "PARENTS"

    invoke-direct {v0, v5, v4}, Lcom/github/javaparser/ast/Node$TreeTraversal;-><init>(Ljava/lang/String;I)V

    sput-object v0, Lcom/github/javaparser/ast/Node$TreeTraversal;->PARENTS:Lcom/github/javaparser/ast/Node$TreeTraversal;

    new-instance v0, Lcom/github/javaparser/ast/Node$TreeTraversal;

    const/4 v5, 0x4

    const-string v6, "DIRECT_CHILDREN"

    invoke-direct {v0, v6, v5}, Lcom/github/javaparser/ast/Node$TreeTraversal;-><init>(Ljava/lang/String;I)V

    sput-object v0, Lcom/github/javaparser/ast/Node$TreeTraversal;->DIRECT_CHILDREN:Lcom/github/javaparser/ast/Node$TreeTraversal;

    const/4 v0, 0x5

    .line 2
    new-array v0, v0, [Lcom/github/javaparser/ast/Node$TreeTraversal;

    sget-object v6, Lcom/github/javaparser/ast/Node$TreeTraversal;->PREORDER:Lcom/github/javaparser/ast/Node$TreeTraversal;

    aput-object v6, v0, v1

    sget-object v1, Lcom/github/javaparser/ast/Node$TreeTraversal;->BREADTHFIRST:Lcom/github/javaparser/ast/Node$TreeTraversal;

    aput-object v1, v0, v2

    sget-object v1, Lcom/github/javaparser/ast/Node$TreeTraversal;->POSTORDER:Lcom/github/javaparser/ast/Node$TreeTraversal;

    aput-object v1, v0, v3

    sget-object v1, Lcom/github/javaparser/ast/Node$TreeTraversal;->PARENTS:Lcom/github/javaparser/ast/Node$TreeTraversal;

    aput-object v1, v0, v4

    sget-object v1, Lcom/github/javaparser/ast/Node$TreeTraversal;->DIRECT_CHILDREN:Lcom/github/javaparser/ast/Node$TreeTraversal;

    aput-object v1, v0, v5

    sput-object v0, Lcom/github/javaparser/ast/Node$TreeTraversal;->a:[Lcom/github/javaparser/ast/Node$TreeTraversal;

    return-void
.end method

.method public constructor <init>(Ljava/lang/String;I)V
    .registers 3
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "()V"
        }
    .end annotation

    .line 1
    invoke-direct {p0, p1, p2}, Ljava/lang/Enum;-><init>(Ljava/lang/String;I)V

    return-void
.end method

.method public static valueOf(Ljava/lang/String;)Lcom/github/javaparser/ast/Node$TreeTraversal;
    .registers 2

    .line 1
    const-class v0, Lcom/github/javaparser/ast/Node$TreeTraversal;

    invoke-static {v0, p0}, Ljava/lang/Enum;->valueOf(Ljava/lang/Class;Ljava/lang/String;)Ljava/lang/Enum;

    move-result-object p0

    check-cast p0, Lcom/github/javaparser/ast/Node$TreeTraversal;

    return-object p0
.end method

.method public static values()[Lcom/github/javaparser/ast/Node$TreeTraversal;
    .registers 1

    .line 1
    sget-object v0, Lcom/github/javaparser/ast/Node$TreeTraversal;->a:[Lcom/github/javaparser/ast/Node$TreeTraversal;

    invoke-virtual {v0}, [Lcom/github/javaparser/ast/Node$TreeTraversal;->clone()Ljava/lang/Object;

    move-result-object v0

    check-cast v0, [Lcom/github/javaparser/ast/Node$TreeTraversal;

    return-object v0
.end method

###### Class com.github.javaparser.ast.Node.a (com.github.javaparser.ast.Node$a)
.class public Lcom/github/javaparser/ast/Node$a;
.super Ljava/lang/Object;
.source "SourceFile"

# interfaces
.implements Ljava/util/Iterator;


# annotations
.annotation system Ldalvik/annotation/EnclosingClass;
    value = Lcom/github/javaparser/ast/Node;
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x9
    name = "a"
.end annotation

.annotation system Ldalvik/annotation/Signature;
    value = {
        "Ljava/lang/Object;",
        "Ljava/util/Iterator<",
        "Lcom/github/javaparser/ast/Node;",
        ">;"
    }
.end annotation


# instance fields
.field public final a:Ljava/util/Queue;
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "Ljava/util/Queue<",
            "Lcom/github/javaparser/ast/Node;",
            ">;"
        }
    .end annotation
.end field


# direct methods
.method public constructor <init>(Lcom/github/javaparser/ast/Node;)V
    .registers 3

    .line 1
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    .line 2
    new-instance v0, Ljava/util/LinkedList;

    invoke-direct {v0}, Ljava/util/LinkedList;-><init>()V

    iput-object v0, p0, Lcom/github/javaparser/ast/Node$a;->a:Ljava/util/Queue;

    .line 3
    iget-object v0, p0, Lcom/github/javaparser/ast/Node$a;->a:Ljava/util/Queue;

    invoke-interface {v0, p1}, Ljava/util/Queue;->add(Ljava/lang/Object;)Z

    return-void
.end method


# virtual methods
.method public hasNext()Z
    .registers 2

    .line 1
    iget-object v0, p0, Lcom/github/javaparser/ast/Node$a;->a:Ljava/util/Queue;

    invoke-interface {v0}, Ljava/util/Queue;->isEmpty()Z

    move-result v0

    xor-int/lit8 v0, v0, 0x1

    return v0
.end method

.method public next()Lcom/github/javaparser/ast/Node;
    .registers 4

    .line 2
    iget-object v0, p0, Lcom/github/javaparser/ast/Node$a;->a:Ljava/util/Queue;

    invoke-interface {v0}, Ljava/util/Queue;->remove()Ljava/lang/Object;

    move-result-object v0

    check-cast v0, Lcom/github/javaparser/ast/Node;

    .line 3
    iget-object v1, p0, Lcom/github/javaparser/ast/Node$a;->a:Ljava/util/Queue;

    invoke-virtual {v0}, Lcom/github/javaparser/ast/Node;->r()Ljava/util/List;

    move-result-object v2

    invoke-interface {v1, v2}, Ljava/util/Queue;->addAll(Ljava/util/Collection;)Z

    return-object v0
.end method

.method public bridge synthetic next()Ljava/lang/Object;
    .registers 2

    .line 1
    invoke-virtual {p0}, Lcom/github/javaparser/ast/Node$a;->next()Lcom/github/javaparser/ast/Node;

    move-result-object v0

    return-object v0
.end method

###### Class com.github.javaparser.ast.Node.b (com.github.javaparser.ast.Node$b)
.class public Lcom/github/javaparser/ast/Node$b;
.super Ljava/lang/Object;
.source "SourceFile"

# interfaces
.implements Ljava/util/Iterator;


# annotations
.annotation system Ldalvik/annotation/EnclosingClass;
    value = Lcom/github/javaparser/ast/Node;
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x9
    name = "b"
.end annotation

.annotation system Ldalvik/annotation/Signature;
    value = {
        "Ljava/lang/Object;",
        "Ljava/util/Iterator<",
        "Lcom/github/javaparser/ast/Node;",
        ">;"
    }
.end annotation


# instance fields
.field public final a:Ljava/util/Iterator;
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "Ljava/util/Iterator<",
            "Lcom/github/javaparser/ast/Node;",
            ">;"
        }
    .end annotation
.end field


# direct methods
.method public constructor <init>(Lcom/github/javaparser/ast/Node;)V
    .registers 3

    .line 1
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    .line 2
    new-instance v0, Ljava/util/ArrayList;

    invoke-virtual {p1}, Lcom/github/javaparser/ast/Node;->r()Ljava/util/List;

    move-result-object p1

    invoke-direct {v0, p1}, Ljava/util/ArrayList;-><init>(Ljava/util/Collection;)V

    invoke-virtual {v0}, Ljava/util/ArrayList;->iterator()Ljava/util/Iterator;

    move-result-object p1

    iput-object p1, p0, Lcom/github/javaparser/ast/Node$b;->a:Ljava/util/Iterator;

    return-void
.end method


# virtual methods
.method public hasNext()Z
    .registers 2

    .line 1
    iget-object v0, p0, Lcom/github/javaparser/ast/Node$b;->a:Ljava/util/Iterator;

    invoke-interface {v0}, Ljava/util/Iterator;->hasNext()Z

    move-result v0

    return v0
.end method

.method public next()Lcom/github/javaparser/ast/Node;
    .registers 2

    .line 2
    iget-object v0, p0, Lcom/github/javaparser/ast/Node$b;->a:Ljava/util/Iterator;

    invoke-interface {v0}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    move-result-object v0

    check-cast v0, Lcom/github/javaparser/ast/Node;

    return-object v0
.end method

.method public bridge synthetic next()Ljava/lang/Object;
    .registers 2

    .line 1
    invoke-virtual {p0}, Lcom/github/javaparser/ast/Node$b;->next()Lcom/github/javaparser/ast/Node;

    move-result-object v0

    return-object v0
.end method

###### Class com.github.javaparser.ast.Node.c (com.github.javaparser.ast.Node$c)
.class public Lcom/github/javaparser/ast/Node$c;
.super Ljava/lang/Object;
.source "SourceFile"

# interfaces
.implements Ljava/util/Iterator;


# annotations
.annotation system Ldalvik/annotation/EnclosingClass;
    value = Lcom/github/javaparser/ast/Node;
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x9
    name = "c"
.end annotation

.annotation system Ldalvik/annotation/Signature;
    value = {
        "Ljava/lang/Object;",
        "Ljava/util/Iterator<",
        "Lcom/github/javaparser/ast/Node;",
        ">;"
    }
.end annotation


# instance fields
.field public a:Lcom/github/javaparser/ast/Node;


# direct methods
.method public constructor <init>(Lcom/github/javaparser/ast/Node;)V
    .registers 2

    .line 1
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    .line 2
    iput-object p1, p0, Lcom/github/javaparser/ast/Node$c;->a:Lcom/github/javaparser/ast/Node;

    return-void
.end method


# virtual methods
.method public hasNext()Z
    .registers 2

    .line 1
    iget-object v0, p0, Lcom/github/javaparser/ast/Node$c;->a:Lcom/github/javaparser/ast/Node;

    invoke-virtual {v0}, Lcom/github/javaparser/ast/Node;->getParentNode()Ljava/util/Optional;

    move-result-object v0

    invoke-virtual {v0}, Ljava/util/Optional;->isPresent()Z

    move-result v0

    return v0
.end method

.method public next()Lcom/github/javaparser/ast/Node;
    .registers 3

    .line 2
    iget-object v0, p0, Lcom/github/javaparser/ast/Node$c;->a:Lcom/github/javaparser/ast/Node;

    invoke-virtual {v0}, Lcom/github/javaparser/ast/Node;->getParentNode()Ljava/util/Optional;

    move-result-object v0

    const/4 v1, 0x0

    invoke-virtual {v0, v1}, Ljava/util/Optional;->orElse(Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, Lcom/github/javaparser/ast/Node;

    iput-object v0, p0, Lcom/github/javaparser/ast/Node$c;->a:Lcom/github/javaparser/ast/Node;

    .line 3
    iget-object v0, p0, Lcom/github/javaparser/ast/Node$c;->a:Lcom/github/javaparser/ast/Node;

    return-object v0
.end method

.method public bridge synthetic next()Ljava/lang/Object;
    .registers 2

    .line 1
    invoke-virtual {p0}, Lcom/github/javaparser/ast/Node$c;->next()Lcom/github/javaparser/ast/Node;

    move-result-object v0

    return-object v0
.end method

###### Class com.github.javaparser.ast.Node.d (com.github.javaparser.ast.Node$d)
.class public Lcom/github/javaparser/ast/Node$d;
.super Ljava/lang/Object;
.source "SourceFile"

# interfaces
.implements Ljava/util/Iterator;


# annotations
.annotation system Ldalvik/annotation/EnclosingClass;
    value = Lcom/github/javaparser/ast/Node;
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x9
    name = "d"
.end annotation

.annotation system Ldalvik/annotation/Signature;
    value = {
        "Ljava/lang/Object;",
        "Ljava/util/Iterator<",
        "Lcom/github/javaparser/ast/Node;",
        ">;"
    }
.end annotation


# instance fields
.field public final a:Ljava/util/Stack;
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "Ljava/util/Stack<",
            "Ljava/util/List<",
            "Lcom/github/javaparser/ast/Node;",
            ">;>;"
        }
    .end annotation
.end field

.field public final b:Ljava/util/Stack;
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "Ljava/util/Stack<",
            "Ljava/lang/Integer;",
            ">;"
        }
    .end annotation
.end field

.field public final c:Lcom/github/javaparser/ast/Node;

.field public d:Z


# direct methods
.method public constructor <init>(Lcom/github/javaparser/ast/Node;)V
    .registers 3

    .line 1
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    .line 2
    new-instance v0, Ljava/util/Stack;

    invoke-direct {v0}, Ljava/util/Stack;-><init>()V

    iput-object v0, p0, Lcom/github/javaparser/ast/Node$d;->a:Ljava/util/Stack;

    .line 3
    new-instance v0, Ljava/util/Stack;

    invoke-direct {v0}, Ljava/util/Stack;-><init>()V

    iput-object v0, p0, Lcom/github/javaparser/ast/Node$d;->b:Ljava/util/Stack;

    const/4 v0, 0x1

    .line 4
    iput-boolean v0, p0, Lcom/github/javaparser/ast/Node$d;->d:Z

    .line 5
    iput-object p1, p0, Lcom/github/javaparser/ast/Node$d;->c:Lcom/github/javaparser/ast/Node;

    .line 6
    invoke-virtual {p0, p1}, Lcom/github/javaparser/ast/Node$d;->a(Lcom/github/javaparser/ast/Node;)V

    return-void
.end method


# virtual methods
.method public final a()Lcom/github/javaparser/ast/Node;
    .registers 5

    .line 6
    iget-object v0, p0, Lcom/github/javaparser/ast/Node$d;->a:Ljava/util/Stack;

    invoke-virtual {v0}, Ljava/util/Stack;->peek()Ljava/lang/Object;

    move-result-object v0

    check-cast v0, Ljava/util/List;

    .line 7
    iget-object v1, p0, Lcom/github/javaparser/ast/Node$d;->b:Ljava/util/Stack;

    invoke-virtual {v1}, Ljava/util/Stack;->pop()Ljava/lang/Object;

    move-result-object v1

    check-cast v1, Ljava/lang/Integer;

    invoke-virtual {v1}, Ljava/lang/Integer;->intValue()I

    move-result v1

    .line 8
    iget-object v2, p0, Lcom/github/javaparser/ast/Node$d;->b:Ljava/util/Stack;

    add-int/lit8 v3, v1, 0x1

    invoke-static {v3}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object v3

    invoke-virtual {v2, v3}, Ljava/util/Stack;->push(Ljava/lang/Object;)Ljava/lang/Object;

    .line 9
    invoke-interface {v0, v1}, Ljava/util/List;->get(I)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, Lcom/github/javaparser/ast/Node;

    return-object v0
.end method

.method public final a(Lcom/github/javaparser/ast/Node;)V
    .registers 5

    .line 1
    :goto_0
    new-instance v0, Ljava/util/ArrayList;

    invoke-virtual {p1}, Lcom/github/javaparser/ast/Node;->r()Ljava/util/List;

    move-result-object p1

    invoke-direct {v0, p1}, Ljava/util/ArrayList;-><init>(Ljava/util/Collection;)V

    .line 2
    invoke-interface {v0}, Ljava/util/List;->isEmpty()Z

    move-result p1

    if-eqz p1, :cond_10

    return-void

    .line 3
    :cond_10
    iget-object p1, p0, Lcom/github/javaparser/ast/Node$d;->a:Ljava/util/Stack;

    invoke-virtual {p1, v0}, Ljava/util/Stack;->push(Ljava/lang/Object;)Ljava/lang/Object;

    .line 4
    iget-object p1, p0, Lcom/github/javaparser/ast/Node$d;->b:Ljava/util/Stack;

    const/4 v1, 0x0

    invoke-static {v1}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object v2

    invoke-virtual {p1, v2}, Ljava/util/Stack;->push(Ljava/lang/Object;)Ljava/lang/Object;

    .line 5
    invoke-interface {v0, v1}, Ljava/util/List;->get(I)Ljava/lang/Object;

    move-result-object p1

    check-cast p1, Lcom/github/javaparser/ast/Node;

    goto :goto_0
.end method

.method public hasNext()Z
    .registers 2

    .line 1
    iget-boolean v0, p0, Lcom/github/javaparser/ast/Node$d;->d:Z

    return v0
.end method

.method public next()Lcom/github/javaparser/ast/Node;
    .registers 5

    .line 2
    iget-object v0, p0, Lcom/github/javaparser/ast/Node$d;->a:Ljava/util/Stack;

    invoke-virtual {v0}, Ljava/util/Stack;->peek()Ljava/lang/Object;

    move-result-object v0

    check-cast v0, Ljava/util/List;

    .line 3
    iget-object v1, p0, Lcom/github/javaparser/ast/Node$d;->b:Ljava/util/Stack;

    invoke-virtual {v1}, Ljava/util/Stack;->peek()Ljava/lang/Object;

    move-result-object v1

    check-cast v1, Ljava/lang/Integer;

    invoke-virtual {v1}, Ljava/lang/Integer;->intValue()I

    move-result v1

    .line 4
    invoke-interface {v0}, Ljava/util/List;->size()I

    move-result v2

    const/4 v3, 0x1

    if-ge v1, v2, :cond_1d

    const/4 v2, 0x1

    goto :goto_1e

    :cond_1d
    const/4 v2, 0x0

    :goto_1e
    if-eqz v2, :cond_2e

    .line 5
    invoke-interface {v0, v1}, Ljava/util/List;->get(I)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, Lcom/github/javaparser/ast/Node;

    .line 6
    invoke-virtual {p0, v0}, Lcom/github/javaparser/ast/Node$d;->a(Lcom/github/javaparser/ast/Node;)V

    .line 7
    invoke-virtual {p0}, Lcom/github/javaparser/ast/Node$d;->a()Lcom/github/javaparser/ast/Node;

    move-result-object v0

    return-object v0

    .line 8
    :cond_2e
    iget-object v0, p0, Lcom/github/javaparser/ast/Node$d;->a:Ljava/util/Stack;

    invoke-virtual {v0}, Ljava/util/Stack;->pop()Ljava/lang/Object;

    .line 9
    iget-object v0, p0, Lcom/github/javaparser/ast/Node$d;->b:Ljava/util/Stack;

    invoke-virtual {v0}, Ljava/util/Stack;->pop()Ljava/lang/Object;

    .line 10
    iget-object v0, p0, Lcom/github/javaparser/ast/Node$d;->a:Ljava/util/Stack;

    invoke-virtual {v0}, Ljava/util/Stack;->empty()Z

    move-result v0

    xor-int/2addr v0, v3

    iput-boolean v0, p0, Lcom/github/javaparser/ast/Node$d;->d:Z

    .line 11
    iget-boolean v0, p0, Lcom/github/javaparser/ast/Node$d;->d:Z

    if-eqz v0, :cond_4a

    .line 12
    invoke-virtual {p0}, Lcom/github/javaparser/ast/Node$d;->a()Lcom/github/javaparser/ast/Node;

    move-result-object v0

    return-object v0

    .line 13
    :cond_4a
    iget-object v0, p0, Lcom/github/javaparser/ast/Node$d;->c:Lcom/github/javaparser/ast/Node;

    return-object v0
.end method

.method public bridge synthetic next()Ljava/lang/Object;
    .registers 2

    .line 1
    invoke-virtual {p0}, Lcom/github/javaparser/ast/Node$d;->next()Lcom/github/javaparser/ast/Node;

    move-result-object v0

    return-object v0
.end method

###### Class com.github.javaparser.ast.Node.e (com.github.javaparser.ast.Node$e)
.class public Lcom/github/javaparser/ast/Node$e;
.super Ljava/lang/Object;
.source "SourceFile"

# interfaces
.implements Ljava/util/Iterator;


# annotations
.annotation system Ldalvik/annotation/EnclosingClass;
    value = Lcom/github/javaparser/ast/Node;
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x9
    name = "e"
.end annotation

.annotation system Ldalvik/annotation/Signature;
    value = {
        "Ljava/lang/Object;",
        "Ljava/util/Iterator<",
        "Lcom/github/javaparser/ast/Node;",
        ">;"
    }
.end annotation


# instance fields
.field public final a:Ljava/util/Stack;
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "Ljava/util/Stack<",
            "Lcom/github/javaparser/ast/Node;",
            ">;"
        }
    .end annotation
.end field


# direct methods
.method public constructor <init>(Lcom/github/javaparser/ast/Node;)V
    .registers 3

    .line 1
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    .line 2
    new-instance v0, Ljava/util/Stack;

    invoke-direct {v0}, Ljava/util/Stack;-><init>()V

    iput-object v0, p0, Lcom/github/javaparser/ast/Node$e;->a:Ljava/util/Stack;

    .line 3
    iget-object v0, p0, Lcom/github/javaparser/ast/Node$e;->a:Ljava/util/Stack;

    invoke-virtual {v0, p1}, Ljava/util/Stack;->add(Ljava/lang/Object;)Z

    return-void
.end method


# virtual methods
.method public hasNext()Z
    .registers 2

    .line 1
    iget-object v0, p0, Lcom/github/javaparser/ast/Node$e;->a:Ljava/util/Stack;

    invoke-virtual {v0}, Ljava/util/Stack;->isEmpty()Z

    move-result v0

    xor-int/lit8 v0, v0, 0x1

    return v0
.end method

.method public next()Lcom/github/javaparser/ast/Node;
    .registers 6

    .line 2
    iget-object v0, p0, Lcom/github/javaparser/ast/Node$e;->a:Ljava/util/Stack;

    invoke-virtual {v0}, Ljava/util/Stack;->pop()Ljava/lang/Object;

    move-result-object v0

    check-cast v0, Lcom/github/javaparser/ast/Node;

    .line 3
    invoke-virtual {v0}, Lcom/github/javaparser/ast/Node;->r()Ljava/util/List;

    move-result-object v1

    .line 4
    invoke-interface {v1}, Ljava/util/List;->size()I

    move-result v2

    add-int/lit8 v2, v2, -0x1

    :goto_12
    if-ltz v2, :cond_20

    .line 5
    iget-object v3, p0, Lcom/github/javaparser/ast/Node$e;->a:Ljava/util/Stack;

    invoke-interface {v1, v2}, Ljava/util/List;->get(I)Ljava/lang/Object;

    move-result-object v4

    invoke-virtual {v3, v4}, Ljava/util/Stack;->add(Ljava/lang/Object;)Z

    add-int/lit8 v2, v2, -0x1

    goto :goto_12

    :cond_20
    return-object v0
.end method

.method public bridge synthetic next()Ljava/lang/Object;
    .registers 2

    .line 1
    invoke-virtual {p0}, Lcom/github/javaparser/ast/Node$e;->next()Lcom/github/javaparser/ast/Node;

    move-result-object v0

    return-object v0
.end method

###### Class defpackage.C0778ct (ct)
.class public final synthetic Lct;
.super Ljava/lang/Object;
.source "lambda"

# interfaces
.implements Ljava/util/function/Consumer;


# instance fields
.field private final synthetic a:Ljava/lang/Class;

.field private final synthetic b:Ljava/util/function/Consumer;


# direct methods
.method public synthetic constructor <init>(Ljava/lang/Class;Ljava/util/function/Consumer;)V
    .registers 3

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    iput-object p1, p0, Lct;->a:Ljava/lang/Class;

    iput-object p2, p0, Lct;->b:Ljava/util/function/Consumer;

    return-void
.end method


# virtual methods
.method public final accept(Ljava/lang/Object;)V
    .registers 4

    iget-object v0, p0, Lct;->a:Ljava/lang/Class;

    iget-object v1, p0, Lct;->b:Ljava/util/function/Consumer;

    check-cast p1, Lcom/github/javaparser/ast/Node;

    invoke-static {v0, v1, p1}, Lcom/github/javaparser/ast/Node;->a(Ljava/lang/Class;Ljava/util/function/Consumer;Lcom/github/javaparser/ast/Node;)V

    return-void
.end method

###### Class defpackage.C0827dt (dt)
.class public final synthetic Ldt;
.super Ljava/lang/Object;
.source "lambda"

# interfaces
.implements Ljava/lang/Iterable;


# instance fields
.field private final synthetic a:Lcom/github/javaparser/ast/Node;

.field private final synthetic b:Lcom/github/javaparser/ast/Node$TreeTraversal;


# direct methods
.method public synthetic constructor <init>(Lcom/github/javaparser/ast/Node;Lcom/github/javaparser/ast/Node$TreeTraversal;)V
    .registers 3

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    iput-object p1, p0, Ldt;->a:Lcom/github/javaparser/ast/Node;

    iput-object p2, p0, Ldt;->b:Lcom/github/javaparser/ast/Node$TreeTraversal;

    return-void
.end method


# virtual methods
.method public final iterator()Ljava/util/Iterator;
    .registers 3

    iget-object v0, p0, Ldt;->a:Lcom/github/javaparser/ast/Node;

    iget-object v1, p0, Ldt;->b:Lcom/github/javaparser/ast/Node$TreeTraversal;

    invoke-virtual {v0, v1}, Lcom/github/javaparser/ast/Node;->a(Lcom/github/javaparser/ast/Node$TreeTraversal;)Ljava/util/Iterator;

    move-result-object v0

    return-object v0
.end method

###### Class defpackage.C0926ft (ft)
.class public final synthetic Lft;
.super Ljava/lang/Object;
.source "lambda"

# interfaces
.implements Ljava/util/function/Consumer;


# instance fields
.field private final synthetic a:Lcom/github/javaparser/ast/observer/AstObserver;


# direct methods
.method public synthetic constructor <init>(Lcom/github/javaparser/ast/observer/AstObserver;)V
    .registers 2

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    iput-object p1, p0, Lft;->a:Lcom/github/javaparser/ast/observer/AstObserver;

    return-void
.end method


# virtual methods
.method public final accept(Ljava/lang/Object;)V
    .registers 3

    iget-object v0, p0, Lft;->a:Lcom/github/javaparser/ast/observer/AstObserver;

    check-cast p1, Lcom/github/javaparser/ast/Node;

    invoke-static {v0, p1}, Lcom/github/javaparser/ast/Node;->a(Lcom/github/javaparser/ast/observer/AstObserver;Lcom/github/javaparser/ast/Node;)V

    return-void
.end method

###### Class defpackage.C0976gt (gt)
.class public final synthetic Lgt;
.super Ljava/lang/Object;
.source "lambda"

# interfaces
.implements Ljava/util/function/Consumer;


# instance fields
.field private final synthetic a:Lcom/github/javaparser/ast/Node;

.field private final synthetic b:Lcom/github/javaparser/ast/Node;


# direct methods
.method public synthetic constructor <init>(Lcom/github/javaparser/ast/Node;Lcom/github/javaparser/ast/Node;)V
    .registers 3

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    iput-object p1, p0, Lgt;->a:Lcom/github/javaparser/ast/Node;

    iput-object p2, p0, Lgt;->b:Lcom/github/javaparser/ast/Node;

    return-void
.end method


# virtual methods
.method public final accept(Ljava/lang/Object;)V
    .registers 4

    iget-object v0, p0, Lgt;->a:Lcom/github/javaparser/ast/Node;

    iget-object v1, p0, Lgt;->b:Lcom/github/javaparser/ast/Node;

    check-cast p1, Lcom/github/javaparser/ast/observer/AstObserver;

    invoke-virtual {v0, v1, p1}, Lcom/github/javaparser/ast/Node;->a(Lcom/github/javaparser/ast/Node;Lcom/github/javaparser/ast/observer/AstObserver;)V

    return-void
.end method

###### Class defpackage.C1025ht (ht)
.class public final synthetic Lht;
.super Ljava/lang/Object;
.source "lambda"

# interfaces
.implements Ljava/util/function/Consumer;


# instance fields
.field private final synthetic a:Lcom/github/javaparser/ast/Node;

.field private final synthetic b:Lcom/github/javaparser/ast/observer/ObservableProperty;

.field private final synthetic c:Ljava/lang/Object;

.field private final synthetic d:Ljava/lang/Object;


# direct methods
.method public synthetic constructor <init>(Lcom/github/javaparser/ast/Node;Lcom/github/javaparser/ast/observer/ObservableProperty;Ljava/lang/Object;Ljava/lang/Object;)V
    .registers 5

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    iput-object p1, p0, Lht;->a:Lcom/github/javaparser/ast/Node;

    iput-object p2, p0, Lht;->b:Lcom/github/javaparser/ast/observer/ObservableProperty;

    iput-object p3, p0, Lht;->c:Ljava/lang/Object;

    iput-object p4, p0, Lht;->d:Ljava/lang/Object;

    return-void
.end method


# virtual methods
.method public final accept(Ljava/lang/Object;)V
    .registers 6

    iget-object v0, p0, Lht;->a:Lcom/github/javaparser/ast/Node;

    iget-object v1, p0, Lht;->b:Lcom/github/javaparser/ast/observer/ObservableProperty;

    iget-object v2, p0, Lht;->c:Ljava/lang/Object;

    iget-object v3, p0, Lht;->d:Ljava/lang/Object;

    check-cast p1, Lcom/github/javaparser/ast/observer/AstObserver;

    invoke-virtual {v0, v1, v2, v3, p1}, Lcom/github/javaparser/ast/Node;->a(Lcom/github/javaparser/ast/observer/ObservableProperty;Ljava/lang/Object;Ljava/lang/Object;Lcom/github/javaparser/ast/observer/AstObserver;)V

    return-void
.end method

###### Class defpackage.C1273mt (mt)
.class public final synthetic Lmt;
.super Ljava/lang/Object;
.source "lambda"

# interfaces
.implements Ljava/util/function/Consumer;


# instance fields
.field private final synthetic a:Ljava/util/List;


# direct methods
.method public synthetic constructor <init>(Ljava/util/List;)V
    .registers 2

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    iput-object p1, p0, Lmt;->a:Ljava/util/List;

    return-void
.end method


# virtual methods
.method public final accept(Ljava/lang/Object;)V
    .registers 3

    iget-object v0, p0, Lmt;->a:Ljava/util/List;

    check-cast p1, Lcom/github/javaparser/ast/Node;

    invoke-interface {v0, p1}, Ljava/util/List;->add(Ljava/lang/Object;)Z

    .sparse-switch
        0x1 -> :L0
    .end sparse-switch 

    return-void
.end method

