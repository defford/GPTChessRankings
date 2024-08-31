import { supabase } from '../lib/supabase';

export async function fetchLadder() {
  const { data, error } = await supabase
    .from('players')
    .select('id, name')
    .order('ladder_position', { ascending: true });

  if (error) throw error;
  return data;
}