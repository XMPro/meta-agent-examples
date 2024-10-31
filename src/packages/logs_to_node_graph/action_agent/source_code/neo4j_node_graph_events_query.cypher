// Using WITH and COLLECT to combine results instead of UNION
CALL {
    // StreamObject query
    MATCH (so:StreamObject)
    RETURN so.node_id AS id,
           so.title AS title,
           labels(so)[0] as subtitle,
           toString(so.event_count) AS mainstat,
           1.0 AS arc__events_complete,
           0.0 AS arc__events_queued
    
    UNION ALL
    
    // DataStream query
    MATCH (ds:DataStream)-[]-(so:StreamObject)
    WITH ds, 
         sum(so.event_count) as event_count_sum,
         max(so.event_count) as max_event_count,
         count(*) as count
    RETURN ds.node_id AS id,
           ds.title AS title,
           labels(ds)[0] as subtitle,
           toString(event_count_sum) as mainstat,
           toFloat(event_count_sum) / (max_event_count * count) as arc__events_complete,
           1 - toFloat(event_count_sum) / (max_event_count * count) as arc__events_queued
           
    UNION ALL
    
    // StreamHost query
    MATCH (sh:StreamHost)-[]-(ds:DataStream)-[]-(so:StreamObject)
    WITH sh, ds, 
         sum(so.event_count) as event_count_sum,
         max(so.event_count) as max_event_count,
         count(*) as count
    WITH sh,
         sum(event_count_sum) as total_event_count,
         sum(max_event_count * count) as total_max_events
    RETURN sh.node_id AS id,
           sh.title AS title,
           labels(sh)[0] as subtitle,
           toString(total_event_count) as mainstat,
           toFloat(total_event_count) / total_max_events as arc__events_complete,
           1 - toFloat(total_event_count) / total_max_events as arc__events_queued
           
    UNION ALL
    
    // Collection query
    MATCH (c:Collection)-[*]-(ds:DataStream)-[]-(so:StreamObject)
    WITH c, ds,
         sum(so.event_count) as event_count_sum,
         max(so.event_count) as max_event_count,
         count(*) as count
    WITH c,
         sum(event_count_sum) as total_event_count,
         sum(max_event_count * count) as total_max_events
    RETURN c.node_id AS id,
           c.title AS title,
           labels(c)[0] as subtitle,
           toString(total_event_count) as mainstat,
           toFloat(total_event_count) / total_max_events as arc__events_complete,
           1 - toFloat(total_event_count) / total_max_events as arc__events_queued
}
RETURN *