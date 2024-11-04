// TODO fix sh logs as duplicate error and debug agent completion events are logged resuling in incomplete results.

// Using WITH and COLLECT to combine results instead of UNION
CALL {
     // StreamObject query
     MATCH (so:StreamObject)
     RETURN so.node_id AS id,
               so.title AS title,
               labels(so)[0] as subtitle,
               toString(so.event_complete_count) AS mainstat,
               CASE so.event_count
                    WHEN 0 THEN 1
                    ELSE 1 - (toFloat(so.event_complete_count)/so.event_count) 
               END AS arc__events_complete,
               0.0 AS arc__events_pending,
               CASE so.event_failed_count
                    WHEN 0 THEN 0.0
                    ELSE 1 - (toFloat(so.event_failed_count)/so.event_failed_count) 
               END AS arc__events_failed

     UNION ALL

     // DataStream query
     MATCH (ds:DataStream)-[]-(so:StreamObject)
     WITH ds, 
          sum(so.event_complete_count) as event_complete_count_sum,
          sum(so.event_failed_count) as event_failed_count_sum,
          max(so.event_count) as max_event_count,
          count(*) as count
     WITH ds.node_id AS id,
               ds.title AS title,
               labels(ds)[0] as subtitle,
               toString(event_complete_count_sum) as mainstat,
               CASE max_event_count
                    WHEN 0 THEN 0.0
                    ELSE toFloat(event_complete_count_sum) / (max_event_count * count) 
               END as events_complete_ratio,
               CASE max_event_count
                    WHEN 0 THEN 0.0
                    ELSE toFloat(event_failed_count_sum) / (max_event_count * count) 
               END as events_failed_ratio
     RETURN id,
          title,
          subtitle,
          mainstat,
          events_complete_ratio as arc__events_complete,
          events_failed_ratio as arc__events_failed,
          1 - events_complete_ratio - events_failed_ratio as arc__events_pending
               
     UNION ALL

     // StreamHost query
     MATCH (sh:StreamHost)-[]-(ds:DataStream)-[]-(so:StreamObject)
     WITH sh, ds, 
          sum(so.event_complete_count) as event_complete_count_sum,
          sum(so.event_failed_count) as event_failed_count_sum,
          max(so.event_count) as max_event_count,
          count(*) as count
     WITH sh,
          sum(event_complete_count_sum) as total_event_complete_count,
          sum(event_failed_count_sum) as total_event_failed_count,
          sum(max_event_count * count) as total_max_event_count
     WITH sh.node_id AS id,
               sh.title AS title,
               labels(sh)[0] as subtitle,
               toString(total_event_complete_count) as mainstat,
               CASE total_max_event_count
                    WHEN 0 THEN 0.0
                    ELSE toFloat(total_event_complete_count) / total_max_event_count 
               END as events_complete_ratio,
               CASE total_max_event_count
                    WHEN 0 THEN 0.0
                    ELSE toFloat(total_event_failed_count) / total_max_event_count 
               END as events_failed_ratio
     RETURN id,
          title,
          subtitle,
          mainstat,
          events_complete_ratio as arc__events_complete,
          events_failed_ratio as arc__events_failed,
          1 - events_complete_ratio - events_failed_ratio as arc__events_pending

     UNION ALL
     
     // Collection query
     MATCH (c:Collection)-[*]-(ds:DataStream)-[]-(so:StreamObject)
     WITH c, ds,
          sum(so.event_complete_count) as event_complete_count_sum,
          sum(so.event_failed_count) as event_failed_count_sum,
          max(so.event_count) as max_event_count,
          count(*) as count
     WITH c,
          sum(event_complete_count_sum) as total_event_complete_count,
          sum(event_failed_count_sum) as total_event_failed_count,
          sum(max_event_count * count) as total_max_event_count
     WITH c.node_id AS id,
               c.title AS title,
               labels(c)[0] as subtitle,
               toString(total_event_complete_count) as mainstat,
               CASE total_max_event_count
                    WHEN 0 THEN 0.0
                    ELSE toFloat(total_event_complete_count) / total_max_event_count 
               END as events_complete_ratio,
               CASE total_max_event_count
                    WHEN 0 THEN 0.0
                    ELSE toFloat(total_event_failed_count) / total_max_event_count 
               END as events_failed_ratio
     RETURN id,
          title,
          subtitle,
          mainstat,
          events_complete_ratio as arc__events_complete,
          events_failed_ratio as arc__events_failed,
          1 - events_complete_ratio - events_failed_ratio as arc__events_pending
}
RETURN *