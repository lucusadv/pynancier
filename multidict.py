from collections import defaultdict
import csv


class IndexedNT(object):
    @classmethod
    def from_csv(cls, filename, named_tuple_cls, index_fields=None):
        ntc = named_tuple_cls
        with open(filename, 'r') as f:
            csvr = csv.reader(f)
            data = [ntc._make(l) for l in csvr]
        obj = cls(data)
        if index_fields is not None:
            obj.set_index(fields)
        return(obj)

    def __init__(self, namedtuples):
        self.data = namedtuples
        flds = namedtuples[0]._fields
        nflds = range(len(flds))
        self._fdict = dict(zip(nflds, flds))
        self._flds = flds
        self._index = {}

    def set(self, *fieldkeys):
        for fkey in fieldkeys:
            if self._index.has_key(fkey):
                continue
            vals = [getattr(nt, fkey) for nt in self.data]
            d = defaultdict(list)
            for i,v in enumerate(vals):
                d[v].append(i)
            self._index[fkey] = d

    def keys(self, field=None):
        if field is None:
            return [(f, d.keys()) for f,d in self._index.items()]
        return self._index[field].keys()

    def items(self, by_field):
        new_fields = list(set(self._flds) - set([by_field]))
        def subset(idx):
            tbl = IndexedNT([self.data[i] for i in idx])
            tbl.set(*new_fields)
            return(tbl)
        fld_dict = self._index[by_field]
        x = [(val, subset(idx)) for val, idx in fld_dict.items()]
        return(x)

    def get(self, **field_values):
        def getindex(fkey, values):
            fld_dict = self._index[fkey]
            if isinstance(values, (list, tuple)):
                idx = set(i for v in values for i in fld_dict[v])
            else:
                idx = set(i for i in fld_dict[values])
            return(idx)
        idx = [getindex(f,v) for f,v in field_values.items()]
        idx = list(set.intersection(*idx))
        if len(idx) == 1:
            return self.data[idx[0]]
        rows = [self.data[i] for i in idx]
        table = IndexedNT(rows)
        return(table)

    def __repr__(self):
        p = (d.__repr__() for d in self.data)
        return('\n'.join(p))

        #else:
        #    l = len(fkey)
        #    if isinstance(values[0], (list, tuple)):
        #        idx = [[get_idx(fkey[i], v[i]) for i in range(l)] for v in values]
        #        idx = set.union(*[set.intersection(*i) for i in idx])
        #    else:
        #        idx = [get_idx(fkey[i], values[i]) for i in range(l)]
        ###        idx = set.intersection(*idx)
