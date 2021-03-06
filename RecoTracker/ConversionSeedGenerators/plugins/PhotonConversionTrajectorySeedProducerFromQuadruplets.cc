#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/Utilities/interface/Exception.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "FWCore/Framework/interface/Event.h"
#include "DataFormats/Common/interface/Handle.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/ConsumesCollector.h"

#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "PhotonConversionTrajectorySeedProducerFromQuadrupletsAlgo.h"


class PhotonConversionTrajectorySeedProducerFromQuadruplets : public edm::EDProducer {
public:
  PhotonConversionTrajectorySeedProducerFromQuadruplets(const edm::ParameterSet& );
  ~PhotonConversionTrajectorySeedProducerFromQuadruplets(){}
  void produce(edm::Event& , const edm::EventSetup& ) override;

private:
  std::string _newSeedCandidates;
  PhotonConversionTrajectorySeedProducerFromQuadrupletsAlgo *_theFinder;
};


PhotonConversionTrajectorySeedProducerFromQuadruplets::
PhotonConversionTrajectorySeedProducerFromQuadruplets(const edm::ParameterSet& conf)
  : _newSeedCandidates(conf.getParameter<std::string>( "newSeedCandidates"))
{
  _theFinder = new PhotonConversionTrajectorySeedProducerFromQuadrupletsAlgo(conf,
	consumesCollector());
  produces<TrajectorySeedCollection>(_newSeedCandidates);

}

void PhotonConversionTrajectorySeedProducerFromQuadruplets::produce(edm::Event& ev, const edm::EventSetup& es)
{
  std::auto_ptr<TrajectorySeedCollection> result( new TrajectorySeedCollection() );  
  try{
    _theFinder->analyze(ev,es);
    if(_theFinder->getTrajectorySeedCollection()->size())
      result->insert(result->end(),
		     _theFinder->getTrajectorySeedCollection()->begin(),
		     _theFinder->getTrajectorySeedCollection()->end());
  }catch(cms::Exception& er){
    edm::LogError("SeedingConversion") << " Problem in the Single Leg Conversion Seed Producer " <<er.what()<<std::endl;
  }catch(std::exception& er){
    edm::LogError("SeedingConversion") << " Problem in the Single Leg Conversion Seed Producer " << er.what()<<std::endl;
  }

  
  edm::LogInfo("debugTrajSeedFromQuadruplets") << " TrajectorySeedCollection size " << result->size();
  ev.put(result, _newSeedCandidates);  
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(PhotonConversionTrajectorySeedProducerFromQuadruplets);
